from typing import Tuple

from apps.Authentication.models import UserProfile
from apps.Chat.models import Participant
from apps.Common.models import ParticipantType


class MetadataUserService:
    def execute(
        self,
        user,
        profile_data,
        participant_data,
    ) -> Tuple[UserProfile, Participant]:
        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults=profile_data,
        )
        participant, _ = Participant.objects.get_or_create(
            user=user,
            defaults={
                "participant_type": ParticipantType.USER,
                **participant_data,
            },
        )
        return profile, participant
