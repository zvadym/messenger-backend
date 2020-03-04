from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/room/<slug:room_name>/', consumers.ChatConsumer),
]
