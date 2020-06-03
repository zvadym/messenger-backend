from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from apps.rooms.models import Room


class MessengerConsumer(AsyncJsonWebsocketConsumer):
    room_id = None

    GROUPS = {
        'my': 'my-{member_id}',  # private member's changes/messages
        'member': 'member-{member_id}',  # public member's changes
        'room': 'room-{room_id}',  # public room's changes
    }

    joined_groups = []

    async def connect(self):
        # Join members group
        await self.join_group(self.GROUPS['my'].format(member_id=self.scope['user'].pk))
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
        lst = list(room.members.values_list('pk', flat=True))

        if room.created_by_id not in lst:
            lst.append(room.created_by_id)

        return lst

    # Receive message from WebSocket
    async def receive_json(self, content, **kwargs):
        if content['type'] == 'room-join':
            try:
                room = await self.get_room(content['id'])
            except Room.DoesNotExist:
                return

            # Check access to the room
            if not room.is_private or self.scope['user'].pk in await self.get_room_members(room):
                group_name = self.GROUPS['room'].format(room_id=room.pk)

                await self.channel_layer.group_add(
                    group_name,
                    self.channel_name
                )
            return

        if content['type'] == 'room-leave':
            return

        if content['type'] == 'member-join':
            await self.channel_layer.group_add(
                self.GROUPS['member'].format(member_id=content['id']),
                self.channel_name
            )
            return

    ########
    # Methods to send message to WebSocket
    ########

    async def websocket_message(self, event):
        print('websocket_message => ', self.channel_name,  event['data'])
        await self.send_json({
            'namespace': 'messenger',
            'action': 'addMessage' if event['data']['created'] else 'updateMessage',
            'data': event['data']['instance_data']
        })

    async def websocket_room(self, event):
        print('websocket_room => ', self.channel_name,  event['data'])
        await self.send_json({
            'namespace': 'messenger',
            'action': 'addRoom' if event['data']['created'] else 'updateRoom',
            'data': event['data']['instance_data']
        })

    async def websocket_member(self, event):
        print('websocket_member => ', self.channel_name,  event['data'])
        await self.send_json({
            'namespace': 'users',
            'action': 'createUser' if event['data']['created'] else 'updateUser',
            'data': event['data']['instance_data']
        })


