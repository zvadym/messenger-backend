from channels.routing import ProtocolTypeRouter, URLRouter
from apps.sockets import routing as app_routing

from .channels_middleware import TokenAuthMiddleware

application = ProtocolTypeRouter({
    'websocket': TokenAuthMiddleware(
        URLRouter(
            app_routing.websocket_urlpatterns
        )
    ),
})
