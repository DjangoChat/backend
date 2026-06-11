from rest_framework import mixins, viewsets

from apps.Chat.models import Message
from apps.Chat.api.v1.serializers import MessageSerializer
from apps.Authorization.permissions import CustomPermission, SubscriptionPermission
from apps.Common.pagination import MessagePagination


class MessageView(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [SubscriptionPermission, CustomPermission]
    pagination_class = [MessagePagination]

    def get_queryset(self):
        chat_id = self.kwargs.get("chat_id")
        return Message.objects.filter(chat=chat_id)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
