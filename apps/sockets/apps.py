from django.apps import AppConfig


class SocketsConfig(AppConfig):
    name = 'apps.sockets'
    verbose_name = 'Sockets'

    def ready(self):
        from . import signals
