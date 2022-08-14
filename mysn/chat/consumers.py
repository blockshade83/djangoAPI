import json
from channels.generic.websocket import AsyncWebsocketConsumer

# consumer class for chat messages
class ChatConsumer(AsyncWebsocketConsumer):
    # function to manage connection
    async def connect(self):
        # get chat room name from url route
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    # function to manage disconnect
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # function to manage receiving of message
    async def receive(self, text_data):
        # convert message received to json
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # distribute message to all members of the channel
        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'chat_message', 'message': message}
        )

    # function to manage receiving event
    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data = json.dumps({
            'message': message
        }))