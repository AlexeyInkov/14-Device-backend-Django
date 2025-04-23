from django.apps import AppConfig


class MyAuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.my_auth"

    def ready(self):
        import apps.my_auth.signals
