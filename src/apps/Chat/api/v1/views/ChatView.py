from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.Authorization.permissions import CustomPermission, SubscriptionPermission
from apps.Chat.api.v1.docs import list_chats_doc, start_chat_doc
from apps.Chat.api.v1.serializers import (
    SimpleChatSerializer,
    StartChatSerializerInput,
    StartChatSerializerResponseOutput,
)
from apps.Chat.models import Chat
from apps.Chat.service import CreateChatService
from apps.Common.filters import ChatFilter
from apps.Common.pagination import ChatPagination


class ChatView(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Chat.objects.active()
    serializer_class = SimpleChatSerializer
    permission_classes = [SubscriptionPermission, CustomPermission]
    filterset_class = ChatFilter
    pagination_class = ChatPagination

    @list_chats_doc
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

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
