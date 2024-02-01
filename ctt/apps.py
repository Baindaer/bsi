from django.apps import AppConfig


class CttConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ctt'

    def ready(self):
        import ctt.templatetags.custom_filters
