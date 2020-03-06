from channels.routing import ProtocolTypeRouter, URLRouter
from apps.rooms import routing as rooms_routing

from .channels_middleware import TokenAuthMiddleware

application = ProtocolTypeRouter({
    'websocket': TokenAuthMiddleware(
        URLRouter(
            rooms_routing.websocket_urlpatterns
        )
    ),
})
