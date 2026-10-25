from django.apps import AppConfig


class DrtcAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'drtc_app'

    def ready(self):
        from django.contrib.auth.signals import user_logged_in
        from drtc_app.security import clear_failed_attempts, get_client_ip

        def on_admin_login_success(sender, request, user, **kwargs):
            if user and (user.is_staff or user.is_superuser):
                ip = get_client_ip(request)
                clear_failed_attempts(ip)

        user_logged_in.connect(on_admin_login_success, dispatch_uid='drtc_clear_failed_attempts')
