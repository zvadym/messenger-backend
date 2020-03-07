from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('general/', consumers.MemberConsumer),
    path('room/<int:room_id>/', consumers.RoomConsumer),
]
