from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from drtc_app.models import AdminLoginAttempt


class Command(BaseCommand):
    help = "Resets admin password to admin123 and clears all rate-limit lockouts"

    def add_arguments(self, parser):
        parser.add_argument(
            '--password',
            type=str,
            default='admin123',
            help='New password for the admin account (default: admin123)',
        )

    def handle(self, *args, **options):
        new_pwd = options['password']
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'drtcservice@gmail.com', 'is_staff': True, 'is_superuser': True}
        )
        user.set_password(new_pwd)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        count = AdminLoginAttempt.objects.count()
        AdminLoginAttempt.objects.all().delete()

        self.stdout.write(self.style.SUCCESS(
            f"Successfully updated superuser 'admin' with password: '{new_pwd}'"
        ))
        self.stdout.write(self.style.SUCCESS(
            f"Cleared {count} failed login attempt(s) from database. All IPs are now unlocked!"
        ))
