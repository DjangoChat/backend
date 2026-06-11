from django.urls import path
from typing import cast, Any

from apps.Chat.api.v1.consumers import (
    ChatListConsumer,
    NotificationConsumer,
    ConversationConsumer,
)

websocket_urlpatterns = [
    path(
        "ws/notifications/",
        cast(Any, NotificationConsumer.as_asgi()),
    ),
    path(
        "ws/chat-list/<str:type_chat>/",
        cast(Any, ChatListConsumer.as_asgi()),
    ),
    path(
        "ws/conversation/<uuid:conversation_id>/",
        cast(Any, ConversationConsumer.as_asgi()),
    ),
]
