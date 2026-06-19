from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.Authorization.permissions import CustomPermission, SubscriptionPermission
from apps.Chat.api.v1.docs import (
    list_chats_doc,
    start_chat_doc,
    list_messages_from_chat,
    list_participants_from_chat,
)
from apps.Chat.api.v1.serializers import (
    ChatSerializer,
    ChatListSerializer,
    StartChatSerializerInput,
    StartChatSerializerResponseOutput,
    ListMessageSerializer,
    ParticipantSerializer,
)
from apps.Chat.models import Chat, Message
from apps.Chat.service import CreateChatService
from apps.Common.filters import ChatFilter
from apps.Common.pagination import ChatPagination, MessagePagination


class ChatView(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = ChatSerializer
    permission_classes = [SubscriptionPermission, CustomPermission]
    filterset_class = ChatFilter
    pagination_class = ChatPagination

    def get_queryset(self):
        return Chat.objects.all_user_chats(self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ChatListSerializer

        return super().get_serializer_class()

    @list_chats_doc
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @start_chat_doc
    @action(
        detail=False,
        methods=["post"],
        permission_classes=[SubscriptionPermission],
    )
    def create_chat_and_assign_participants(self, request):
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

    @list_messages_from_chat
    @action(
        detail=True,
        methods=["get"],
        permission_classes=[SubscriptionPermission],
        serializer_class=ListMessageSerializer,
        pagination_class=MessagePagination,
    )
    def messages(self, request, pk=None):
        chat = self.get_object()
        participant = request.user.participant

        if not ChatParticipant.objects.filter(
            chat=chat,
            participant=participant,
        ).exists():
            raise PermissionDenied()

        queryset = Message.objects.filter(chat=chat)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ListMessageSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ListMessageSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @list_participants_from_chat
    @action(
        detail=True,
        methods=["get"],
        permission_classes=[SubscriptionPermission],
    )
    def participants(self, request, pk=None):
        chat = self.get_object()
        participant = request.user.participant

        if not ChatParticipant.objects.filter(
            chat=chat,
            participant=participant,
        ).exists():
            raise PermissionDenied()

        queryset = Participant.objects.filter(chatparticipant__chat=chat)
        serializer = ParticipantSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
