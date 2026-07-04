from typing import Any, cast

from django.urls import path

from apps.Chat.api.v1.consumers import ChatConsumer, NotificationConsumer

websocket_urlpatterns = [
    path(
        "ws/notifications/",
        cast(Any, NotificationConsumer.as_asgi()),
    ),
    path(
        "ws/chat/<uuid:chat_id>/",
        cast(Any, ChatConsumer.as_asgi()),
    ),
]
