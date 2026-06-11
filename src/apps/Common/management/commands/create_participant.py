from typing import Any

from django.core.management.base import BaseCommand
from apps.Common.models import AgentName, ParticipantType
from apps.Chat.models import Agent, Participant


class Command(BaseCommand):

    help = "Command for creating all the participants for agents"

    def handle(self, *args: Any, **options: Any) -> str | None:
        for name in AgentName:
            current_agent = Agent.objects.get(name=name)
            Participant.objects.get_or_create(
                participaty_type=ParticipantType.AGENT,
                agent=current_agent,
            )
