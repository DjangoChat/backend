import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class NotificationConsumer(WebsocketConsumer):

    def connect(self):
        self.user = self.scope["user"]  # type: ignore

        # if not self.user.is_authenticated:  # type: ignore
        #     self.close()
        #     return

        self.notification_group = f"notification_user_{self.user.id}"  # type: ignore

        async_to_sync(self.channel_layer.group_add)(
            self.notification_group, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.notification_group, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        self.send(text_data=json.dumps({"message": message}))
