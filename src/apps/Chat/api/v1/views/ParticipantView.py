from rest_framework import mixins, viewsets

from apps.Authorization.permissions import CustomPermission, SubscriptionPermission
from apps.Chat.api.v1.docs import list_participant_doc
from apps.Chat.api.v1.serializers import ParticipantSerializer
from apps.Chat.api.v1.serializers.ChatSerializer import BasicParticipantSerializer
from apps.Chat.models import Participant
from apps.Chat.selectors import participant_list_for_user
from apps.Common.filters import ParticipantFilter
from apps.Common.models import ParticipantRepresentation


class ParticipantView(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [SubscriptionPermission, CustomPermission]
    filterset_class = ParticipantFilter
    search_fields = ["nickname"]

    def get_serializer_class(self):
        representation = self.request.query_params.get("representation")  # type: ignore

        if representation == ParticipantRepresentation.BRIEF:
            return BasicParticipantSerializer

        return self.serializer_class

    def get_queryset(self):
        if self.action == "list":
            return participant_list_for_user(self.request.user)  # type: ignore
        return super().get_queryset()

    @list_participant_doc
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
