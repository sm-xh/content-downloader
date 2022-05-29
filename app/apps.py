from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'


class django_content_downloaderAppConfig(AppConfig):
    name = 'django_content_downloader'
    verbose_name = 'Django YouTube Downloader App'
