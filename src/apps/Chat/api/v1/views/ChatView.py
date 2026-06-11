from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from apps.Authorization.permissions import SubscriptionPermission
from apps.Chat.service import CreateChatService
from apps.Chat.api.v1.serializers import (
    StartChatSerializerInput,
    StartChatSerializerResponseOutput,
)
from apps.Chat.api.v1.docs import start_chat_doc


class ChatView(viewsets.GenericViewSet):

    @start_chat_doc
    @action(
        detail=False,
        methods=["post"],
        permission_classes=[SubscriptionPermission],
    )
    def start_chat(self, request):
        serializer = StartChatSerializerInput(data=request.data)
        serializer.is_valid(raise_exception=True)
        chat, created = CreateChatService().execute(
            current_participant=request.user,
            other_participant_id=serializer.validated_data["participant_id"],  # type: ignore
        )
        response = StartChatSerializerResponseOutput(
            data={"chat_id": chat.id, "created": created}
        )
        return Response(
            response,
            status=status.HTTP_200_OK,
        )
