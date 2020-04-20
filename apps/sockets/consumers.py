import channels.layers
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync

from django.db.models import signals
from django.dispatch import receiver

from apps.api.serializers import MessageSerializer
from apps.members.models import User
from apps.rooms.models import Room, Message


class MessengerConsumer(AsyncJsonWebsocketConsumer):
    room_id = None

    GROUPS = {
        'common': 'member-{member_id}',
        'room': 'room-{room_id}',
    }

    joined_groups = []

    async def connect(self):
        # Join members group
        await self.join_group(self.GROUPS['common'].format(member_id=self.scope['user'].pk))
        await self.accept()

    async def disconnect(self, close_code):
        # Leave all joined groups
        for group in self.joined_groups:
            self.channel_layer.group_discard(
                group,
                self.channel_name
            )

    def join_group(self, group_name):
        self.joined_groups.append(group_name)
        return self.channel_layer.group_add(
            group_name,
            self.channel_name
        )

    @database_sync_to_async
    def get_room(self, pk):
        return Room.objects.get(pk=pk)

    @database_sync_to_async
    def get_room_members(self, room):
        return list(room.members.values_list('pk', flat=True))

    # Receive message from WebSocket
    async def receive_json(self, content, **kwargs):
        if content['type'] == 'room-join':
            try:
                room = await self.get_room(content['id'])
            except Room.DoesNotExist:
                return

            members = await self.get_room_members(room)

            # Check access to the room
            if not room.is_private or self.scope['user'].pk in members:
                group_name = self.GROUPS['room'].format(room_id=room.pk)

                await self.channel_layer.group_add(
                    group_name,
                    self.channel_name
                )
            return

        if content['type'] == 'room-leave':
            return

    async def websocket_message(self, event):
        # Send message to WebSocket
        print('websocket_message => ', self.channel_name,  event['data'])
        await self.send_json(event['data'])

    @staticmethod
    # @receiver(signals.post_save, sender=Room)
    def room_observer(sender, instance, created, **kwargs):
        layer = channels.layers.get_channel_layer()

        def _send(group_name):
            async_to_sync(layer.group_send)(group_name, {
                'type': 'websocket.message',
                'data': {
                    'text': 'Room is updated!',
                    'id': instance.pk
                }
            })

        if instance.is_private:
            for member in instance.members.all():
                if member.is_online:
                    _send(MessengerConsumer.GROUPS['rooms'].format(member_id=member.id))
        else:
            for member in User.objects.all():
                # TODO: find only "online" members
                if member.is_online:
                    _send(MessengerConsumer.GROUPS['rooms'].format(member_id=member.id))

    @staticmethod
    @receiver(signals.post_save, sender=Message)
    def message_observer(sender, instance, created, **kwargs):
        if not created:
            # TODO: handle updated (edited) messages
            return

        layer = channels.layers.get_channel_layer()
        room = instance.room

        async_to_sync(layer.group_send)(
            MessengerConsumer.GROUPS['room'].format(room_id=room.id),
            {
                'type': 'websocket.message',
                'data': {
                    'namespace': 'messenger',
                    'action': 'addMessage',
                    'message': MessageSerializer(instance).data
                }
            }
        )
