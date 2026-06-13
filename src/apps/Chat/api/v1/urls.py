from django.urls import include, path

from apps.Chat.api.v1.views import ChatView, MessageView, NatureDropDownView

urlpatterns = [
    path(
        "natures/",
        NatureDropDownView.as_view({"get": "list"}),
    ),
    path(
        "chats/",
        include(
            [
                path("", ChatView.as_view({"get": "list"})),
                path(
                    "start/",
                    ChatView.as_view({"post": "start_chat"}),
                ),
                path(
                    "<uuid:chat_id>/messages/",
                    MessageView.as_view({"get": "list"}),
                ),
            ]
        ),
    ),
]
