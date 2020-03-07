from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer


class MemberConsumer(WebsocketConsumer):
    user = None

    def connect(self):
        self.username = "Anonymous"

        self.accept()
        self.send(text_data="[Welcome %s!]" % self.username)

    def receive(self, *, text_data):
        if text_data.startswith("/name"):
            self.username = text_data[5:].strip()

            self.send(text_data="[set your username to %s]" % self.username)
        else:
            self.send(text_data=self.username + ": " + text_data)

    def disconnect(self, message):
        pass


class RoomConsumer(AsyncJsonWebsocketConsumer):
    room_id = None
    group_name = None

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.group_name = 'group-room-{}'.format(self.room_id)

        # Join room group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive_json(self, content, **kwargs):
        message = content['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'websocket.message',
                'content': 'RE: ' + message,
            }
        )

    # Receive message from room group
    async def websocket_message(self, event):
        message = event['content']

        # Send message to WebSocket
        await self.send_json({
            'message': message,
            'user_id': self.scope['user'].pk,
        })
