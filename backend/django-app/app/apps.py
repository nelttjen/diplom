from django.apps import AppConfig as DefaultConfig


class AppConfig(DefaultConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
