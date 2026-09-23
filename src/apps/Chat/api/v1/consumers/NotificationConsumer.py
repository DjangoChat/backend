import json

from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]  # type: ignore
        self.notification_socket_name = f"notification__{self.user.id}"  # type: ignore

        await self.channel_layer.group_add(
            self.notification_socket_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.notification_socket_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.send(text_data=json.dumps({"message": message}))

    async def chat_message(self, event):
        """
        Handler for messages sent via the channel layer (from signals).
        Broadcasts the event to the connected client.
        """
        await self.send(
            text_data=json.dumps(
                {
                    "type": "chat_updated",
                    "data": event.get("data"),
                }
            )
        )
