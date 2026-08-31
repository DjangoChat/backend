from django_filters import FilterSet, ChoiceFilter

from apps.Chat.models import Participant
from apps.Common.models import ParticipantRepresentation


class ParticipantFilter(FilterSet):

    representation = ChoiceFilter(
        choices=ParticipantRepresentation.choices,
        method="filter_representation",
    )

    def filter_representation(self, queryset, name, value):
        # Filter participants by their representation type
        # Note: The actual serializer switching happens in ParticipantView.get_serializer_class()
        # This filter can be used to filter the queryset if needed
        return queryset

    class Meta:
        model = Participant
        fields = [
            "participant_type",
            "representation",
        ]
