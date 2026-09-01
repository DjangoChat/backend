from django.db.models import QuerySet

from apps.Authentication.models import CustomUser
from apps.Chat.models import Participant
from apps.Common.models import ParticipantType


def participant_list_for_user(user: CustomUser) -> QuerySet[Participant]:
    try:
        user_participant = Participant.objects.get(user=user)
    except Participant.DoesNotExist:
        user_participant = None

    queryset = Participant.objects.filter(
        participant_type=ParticipantType.AGENT,
    )

    if user_participant:
        user_contacts = Participant.objects.filter(contact_of__owner=user_participant)
        queryset = queryset | user_contacts

    return queryset.distinct()
