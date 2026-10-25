from datetime import timedelta
from django.utils import timezone
from django.contrib.admin.forms import AdminAuthenticationForm
from django.core.exceptions import ValidationError
from .models import AdminLoginAttempt

# Rate limiting security configuration
MAX_FAILED_ATTEMPTS = 5         # Maximum allowed bad password attempts
LOCKOUT_MINUTES = 30           # Minutes the IP remains blocked after exceeding max attempts
FAILURE_WINDOW_MINUTES = 15    # Window in minutes to accumulate failed attempts


def get_client_ip(request):
    """
    Extracts the genuine client IP address, handling proxies, load balancers,
    and serverless environments (e.g. Vercel, Supabase, Cloudflare).
    """
    if not request:
        return '127.0.0.1'
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '127.0.0.1')


def get_ip_attempt_status(ip_address):
    """
    Checks if an IP address is currently locked out or how many recent failures exist.
    Returns: (is_locked: bool, remaining_minutes: int, failure_count: int)
    """
    now = timezone.now()
    lockout_threshold = now - timedelta(minutes=LOCKOUT_MINUTES)
    window_threshold = now - timedelta(minutes=FAILURE_WINDOW_MINUTES)

    # Fetch attempts within the lockout period
    recent_attempts = list(
        AdminLoginAttempt.objects.filter(
            ip_address=ip_address,
            attempted_at__gte=lockout_threshold
        ).order_by('-attempted_at')
    )

    total_recent = len(recent_attempts)

    if total_recent >= MAX_FAILED_ATTEMPTS:
        # Check timestamp of the 5th attempt (the one that triggered lockout)
        trigger_attempt = recent_attempts[MAX_FAILED_ATTEMPTS - 1]
        locked_until = trigger_attempt.attempted_at + timedelta(minutes=LOCKOUT_MINUTES)
        if now < locked_until:
            remaining_seconds = int((locked_until - now).total_seconds())
            remaining_minutes = max(1, (remaining_seconds + 59) // 60)
            return True, remaining_minutes, total_recent

    # Count failures strictly within active window
    active_window_count = sum(1 for a in recent_attempts if a.attempted_at >= window_threshold)
    return False, 0, active_window_count


def record_failed_attempt(request, username):
    """Logs a failed login attempt into the database for audit and rate-limiting."""
    ip = get_client_ip(request)
    ua = request.META.get('HTTP_USER_AGENT', '') if request else ''
    AdminLoginAttempt.objects.create(
        ip_address=ip,
        username=username or 'unknown',
        user_agent=ua[:500]
    )


def clear_failed_attempts(ip_address):
    """Cleans up failure records for an IP upon successful verified authentication."""
    AdminLoginAttempt.objects.filter(ip_address=ip_address).delete()


class SecureAdminAuthenticationForm(AdminAuthenticationForm):
    """
    Enhanced Admin Authentication Form that enforces:
    1. Immediate lockout check before processing credentials.
    2. Failure count increment on invalid credentials.
    3. Clear security alerts and warnings on remaining attempts.
    """
    def clean(self):
        ip = get_client_ip(self.request)
        is_locked, remaining_mins, _ = get_ip_attempt_status(ip)

        if is_locked:
            raise ValidationError(
                f"🚨 Security Lockout: Multiple failed login attempts detected. "
                f"Access from this device/IP ({ip}) is blocked for {remaining_mins} more minute(s) "
                f"to prevent unauthorized access.",
                code='locked_out'
            )

        try:
            return super().clean()
        except ValidationError:
            raw_username = self.data.get('username', '').strip()
            record_failed_attempt(self.request, raw_username)

            now_locked, now_remaining, count = get_ip_attempt_status(ip)
            if now_locked:
                raise ValidationError(
                    f"🚨 Security Alert: Maximum 5 failed attempts exceeded! "
                    f"This IP ({ip}) has now been locked out for {now_remaining} minutes.",
                    code='locked_out'
                )
            else:
                remaining = max(1, MAX_FAILED_ATTEMPTS - count)
                raise ValidationError(
                    f"Invalid operator credentials. "
                    f"⚠️ Security Notice: {remaining} attempt(s) remaining before automatic 30-minute lockout.",
                    code='invalid_login'
                )
