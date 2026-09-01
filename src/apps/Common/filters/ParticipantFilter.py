from django_filters import FilterSet, ChoiceFilter

from apps.Chat.models import Participant
from apps.Common.models import ParticipantRepresentation


class ParticipantFilter(FilterSet):

    representation = ChoiceFilter(
        choices=ParticipantRepresentation.choices,
        method="filter_representation",
    )

    def filter_representation(self, queryset, name, value):
        return queryset

    class Meta:
        model = Participant
        fields = [
            "participant_type",
            "representation",
            "agent__agent_type",
            "agent__natures__name",
        ]
