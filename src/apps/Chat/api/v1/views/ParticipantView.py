from rest_framework import mixins, viewsets

from apps.Authorization.permissions import CustomPermission, SubscriptionPermission
from apps.Chat.models import Participant
from apps.Chat.api.v1.serializers import ParticipantSerializer
from apps.Chat.api.v1.docs import list_participant_doc


class ParticipantView(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [SubscriptionPermission, CustomPermission]
    filterset_fields = ["participant_type"]
    search_fields = ["nickname"]

    @list_participant_doc
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
