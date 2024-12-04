from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json

document_state = {}

class EditorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.doc_id = self.scope["url_route"]["kwargs"]["doc_id"]
        self.room_group_name = f"editor_{self.doc_id}"

        if self.doc_id not in document_state:
            document_state[self.doc_id] = {"ops": []}

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Send current state to the client
        await self.send(text_data=json.dumps({
            "type": "init",
            "content": document_state[self.doc_id]
        }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        if "content" in data:
            # Broadcast changes to other users in the room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "update_content",
                    "content": data["content"],
                    "sender": self.channel_name  # Include sender info
                }
            )

        if "cursor" in data:
            # Broadcast cursor position updates
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "cursor_position",
                    "cursor": data["cursor"],
                    "sender": self.channel_name
                }
            )

    async def update_content(self, event):
        if event["sender"] != self.channel_name:
            await self.send(text_data=json.dumps({
                "type": "update",
                "content": event["content"]
            }))

    async def cursor_position(self, event):
        if event["sender"] != self.channel_name:
            await self.send(text_data=json.dumps({
                "type": "cursor",
                "cursor": event["cursor"]
            }))
