from django.apps import AppConfig


class UseridConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userid'
    def ready(self):
        import userid.signals