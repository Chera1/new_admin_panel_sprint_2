from django.apps import AppConfig


class MoviesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'


class AppsConfig(AppConfig):

    def ready(self):
        import movies.signals
