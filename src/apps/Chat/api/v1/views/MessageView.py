from rest_framework import mixins, viewsets

from apps.Authorization.permissions import CustomPermission, SubscriptionPermission
from apps.Chat.api.v1.serializers import MessageSerializer
from apps.Chat.api.v1.docs import create_message, update_message, partial_update_message
from apps.Chat.models import Message
from apps.Chat.service import CreateMessageService


class MessageView(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [SubscriptionPermission, CustomPermission]

    def perform_create(self, serializer):
        user = self.request.user
        CreateMessageService().execute(
            serializer,
            user,
        )

    @create_message
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @update_message
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @partial_update_message
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
