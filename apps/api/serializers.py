from rest_framework import serializers

from apps.members.models import User
from apps.rooms.models import Room, Message, Notification

from .fields import MessageField


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'last_action_dt',
        )


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            'id',
            'message',
            'room_id',
            'created_by',
            'created_dt',
        )
        read_only_fields = (
            'id',
            'created_by',
            'created_dt'
        )


class RoomSerializer(serializers.ModelSerializer):
    last_message = MessageField()
    updated_dt = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Room
        fields = (
            'id',
            'title',
            'last_message',
            'created_dt',
            'created_by',
            'members',
            'is_private',
            'updated_dt',
        )
        read_only_fields = (
            'id',
            'last_message',
            'created_dt',
            'created_by',
        )


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            'id',
            'message',
            'room_id',
            'created_dt',
        )
        read_only_fields = (
            'id',
            'created_dt'
        )
