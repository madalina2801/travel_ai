from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'travel_project.users'

    def ready(self):
        import travel_project.users.signals