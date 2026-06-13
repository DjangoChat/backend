from rest_framework import mixins, viewsets

from apps.Authorization.permissions import CustomPermission, SubscriptionPermission
from apps.Chat.api.v1.docs import list_messages_doc
from apps.Chat.api.v1.serializers import MessageSerializer
from apps.Chat.models import Message
from apps.Common.pagination import MessagePagination


class MessageView(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [SubscriptionPermission, CustomPermission]
    pagination_class = MessagePagination

    def get_queryset(self):
        chat_id = self.kwargs.get("chat_id")
        return Message.objects.filter(chat=chat_id)

    @list_messages_doc
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
