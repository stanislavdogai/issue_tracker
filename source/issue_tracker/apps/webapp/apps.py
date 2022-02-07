from django.apps import AppConfig


class WebappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'issue_tracker.apps.webapp'
    verbose_name = 'Трекер задач'
