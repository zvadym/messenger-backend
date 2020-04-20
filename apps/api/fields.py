from rest_framework import serializers


class MessageField(serializers.ReadOnlyField):
    def to_representation(self, obj):
        from .serializers import MessageSerializer
        return MessageSerializer(obj).data if obj else None
