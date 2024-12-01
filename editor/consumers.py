# editor/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class EditorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.doc_id = self.scope['url_route']['kwargs']['doc_id']
        self.room_group_name = f"editor_{self.doc_id}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket (client-side will send messages like cursor movements)
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type', '')

        # Send message to room group (send to other connected users)
        if message_type == 'cursor':
            cursor_position = text_data_json.get('cursor_position')
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'cursor_position',
                    'cursor_position': cursor_position,
                }
            )

    # Receive message from room group (send to the WebSocket client)
    async def cursor_position(self, event):
        cursor_position = event['cursor_position']
        await self.send(text_data=json.dumps({
            'type': 'cursor_position',
            'cursor_position': cursor_position,
        }))

