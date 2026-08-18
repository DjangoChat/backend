from rest_framework import mixins, viewsets

from apps.Authorization.permissions import CustomPermission, SubscriptionPermission
from apps.Chat.api.v1.docs import list_natures_doc
from apps.Chat.api.v1.serializers import NatureSerializer
from apps.Chat.models import Nature


class NatureView(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Nature.objects.all()
    serializer_class = NatureSerializer
    permission_classes = [SubscriptionPermission, CustomPermission]

    @list_natures_doc
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
