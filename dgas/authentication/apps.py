from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    name = 'dgas.authentication'
    verbose_name = "Authentication"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
