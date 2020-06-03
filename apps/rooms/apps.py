from django.apps import AppConfig


class RoomConfig(AppConfig):
    name = 'apps.rooms'
    verbose_name = 'Rooms'

    def ready(self):
        from . import signals
