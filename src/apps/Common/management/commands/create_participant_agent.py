import random
from typing import Any

from django.core.management.base import BaseCommand

from apps.Chat.models import Agent, Nature, Participant
from apps.Common.models import AgentName, AgentType, NatureType, ParticipantType

AGENT_BLUEPRINTS = {
    # ======================================================
    # BASIC (8 agents)
    # ======================================================
    AgentName.ALEX: {
        "type": AgentType.BASIC,
        "natures": [
            NatureType.CURIOUS,
            NatureType.COMMUNICATIVE,
            NatureType.CALM,
        ],
    },
    AgentName.JORDAN: {
        "type": AgentType.BASIC,
        "natures": [
            NatureType.LOGICAL,
            NatureType.PRAGMATIC,
            NatureType.DETAIL_ORIENTED,
        ],
    },
    AgentName.CASEY: {
        "type": AgentType.BASIC,
        "natures": [
            NatureType.CREATIVE,
            NatureType.CURIOUS,
            NatureType.ADAPTIVE,
        ],
    },
    AgentName.MORGAN: {
        "type": AgentType.BASIC,
        "natures": [
            NatureType.EMPATHETIC,
            NatureType.SUPPORTIVE,
            NatureType.CALM,
        ],
    },
    AgentName.DAKOTA: {
        "type": AgentType.BASIC,
        "natures": [
            NatureType.ENERGETIC,
            NatureType.PROACTIVE,
            NatureType.ASSERTIVE,
        ],
    },
    AgentName.PARKER: {
        "type": AgentType.BASIC,
        "natures": [
            NatureType.ANALYTICAL,
            NatureType.LOGICAL,
            NatureType.DETAIL_ORIENTED,
        ],
    },
    AgentName.TAYLOR: {
        "type": AgentType.BASIC,
        "natures": [
            NatureType.ADAPTIVE,
            NatureType.COMMUNICATIVE,
            NatureType.CURIOUS,
        ],
    },
    AgentName.BLAKE: {
        "type": AgentType.BASIC,
        "natures": [
            NatureType.ASSERTIVE,
            NatureType.DECISIVE,
            NatureType.PROACTIVE,
        ],
    },
    # ======================================================
    # MEDIUM (9 agents)
    # ======================================================
    AgentName.RORY: {
        "type": AgentType.MEDIUM,
        "natures": [
            NatureType.CURIOUS,
            NatureType.INTUITIVE,
            NatureType.REFLECTIVE,
            NatureType.ANALYTICAL,
            NatureType.ADAPTIVE,
        ],
    },
    AgentName.REAGAN: {
        "type": AgentType.MEDIUM,
        "natures": [
            NatureType.PRINCIPLED,
            NatureType.ASSERTIVE,
            NatureType.RELIABLE,
            NatureType.PRAGMATIC,
            NatureType.DECISIVE,
        ],
    },
    AgentName.BROOKLYN: {
        "type": AgentType.MEDIUM,
        "natures": [
            NatureType.COMMUNICATIVE,
            NatureType.SUPPORTIVE,
            NatureType.ADAPTIVE,
            NatureType.CURIOUS,
            NatureType.REFLECTIVE,
        ],
    },
    AgentName.ARIEL: {
        "type": AgentType.MEDIUM,
        "natures": [
            NatureType.CREATIVE,
            NatureType.INNOVATIVE,
            NatureType.INTUITIVE,
            NatureType.REFLECTIVE,
            NatureType.CURIOUS,
        ],
    },
    AgentName.SAGE: {
        "type": AgentType.MEDIUM,
        "natures": [
            NatureType.ANALYTICAL,
            NatureType.LOGICAL,
            NatureType.REFLECTIVE,
            NatureType.PRAGMATIC,
            NatureType.DETAIL_ORIENTED,
        ],
    },
    AgentName.PHOENIX: {
        "type": AgentType.MEDIUM,
        "natures": [
            NatureType.ENERGETIC,
            NatureType.PROACTIVE,
            NatureType.INNOVATIVE,
            NatureType.VISIONARY,
            NatureType.ADAPTIVE,
        ],
    },
    AgentName.SKYE: {
        "type": AgentType.MEDIUM,
        "natures": [
            NatureType.CALM,
            NatureType.INTUITIVE,
            NatureType.REFLECTIVE,
            NatureType.CURIOUS,
            NatureType.COMMUNICATIVE,
        ],
    },
    AgentName.RIVER: {
        "type": AgentType.MEDIUM,
        "natures": [
            NatureType.ADAPTIVE,
            NatureType.COMMUNICATIVE,
            NatureType.CURIOUS,
            NatureType.PRAGMATIC,
            NatureType.SUPPORTIVE,
        ],
    },
    AgentName.CAMERON: {
        "type": AgentType.MEDIUM,
        "natures": [
            NatureType.ANALYTICAL,
            NatureType.LOGICAL,
            NatureType.DETAIL_ORIENTED,
            NatureType.PRAGMATIC,
            NatureType.REFLECTIVE,
        ],
    },
    # ======================================================
    # ADVANCE (8 agents)
    # ======================================================
    AgentName.AVERY: {
        "type": AgentType.ADVANCE,
        "natures": [
            NatureType.INNOVATIVE,
            NatureType.VISIONARY,
            NatureType.PROACTIVE,
            NatureType.ANALYTICAL,
            NatureType.REFLECTIVE,
            NatureType.ADAPTIVE,
            NatureType.COMMUNICATIVE,
            NatureType.PRAGMATIC,
            NatureType.DETAIL_ORIENTED,
            NatureType.CURIOUS,
        ],
    },
    AgentName.EDEN: {
        "type": AgentType.ADVANCE,
        "natures": [
            NatureType.EMPATHETIC,
            NatureType.SUPPORTIVE,
            NatureType.CALM,
            NatureType.REFLECTIVE,
            NatureType.ADAPTIVE,
            NatureType.COMMUNICATIVE,
            NatureType.PRINCIPLED,
            NatureType.RELIABLE,
            NatureType.PATIENT,
            NatureType.INTUITIVE,
        ],
    },
    AgentName.HAYDEN: {
        "type": AgentType.ADVANCE,
        "natures": [
            NatureType.LOGICAL,
            NatureType.ANALYTICAL,
            NatureType.CRITICAL_THINKING,
            NatureType.PRAGMATIC,
            NatureType.RELIABLE,
            NatureType.PROACTIVE,
            NatureType.REFLECTIVE,
            NatureType.INDEPENDENT,
            NatureType.DECISIVE,
            NatureType.DETAIL_ORIENTED,
        ],
    },
    AgentName.ROBIN: {
        "type": AgentType.ADVANCE,
        "natures": [
            NatureType.CREATIVE,
            NatureType.INNOVATIVE,
            NatureType.VISIONARY,
            NatureType.CURIOUS,
            NatureType.INTUITIVE,
            NatureType.ADAPTIVE,
            NatureType.COMMUNICATIVE,
            NatureType.PROACTIVE,
            NatureType.REFLECTIVE,
            NatureType.ANALYTICAL,
        ],
    },
    AgentName.PEYTON: {
        "type": AgentType.ADVANCE,
        "natures": [
            NatureType.ASSERTIVE,
            NatureType.DECISIVE,
            NatureType.PRAGMATIC,
            NatureType.PROACTIVE,
            NatureType.RELIABLE,
            NatureType.PRINCIPLED,
            NatureType.LOGICAL,
            NatureType.INDEPENDENT,
            NatureType.ANALYTICAL,
            NatureType.REFLECTIVE,
        ],
    },
    AgentName.QUINN: {
        "type": AgentType.ADVANCE,
        "natures": [
            NatureType.CURIOUS,
            NatureType.INTUITIVE,
            NatureType.REFLECTIVE,
            NatureType.ADAPTIVE,
            NatureType.VISIONARY,
            NatureType.INNOVATIVE,
            NatureType.COMMUNICATIVE,
            NatureType.PROACTIVE,
            NatureType.ANALYTICAL,
            NatureType.PRAGMATIC,
        ],
    },
    AgentName.TATUM: {
        "type": AgentType.ADVANCE,
        "natures": [
            NatureType.CALM,
            NatureType.PATIENT,
            NatureType.SUPPORTIVE,
            NatureType.EMPATHETIC,
            NatureType.REFLECTIVE,
            NatureType.ADAPTIVE,
            NatureType.COMMUNICATIVE,
            NatureType.PRINCIPLED,
            NatureType.RELIABLE,
            NatureType.INTUITIVE,
        ],
    },
    AgentName.REECE: {
        "type": AgentType.ADVANCE,
        "natures": [
            NatureType.ENERGETIC,
            NatureType.PROACTIVE,
            NatureType.ASSERTIVE,
            NatureType.DECISIVE,
            NatureType.INNOVATIVE,
            NatureType.VISIONARY,
            NatureType.ADAPTIVE,
            NatureType.ANALYTICAL,
            NatureType.PRAGMATIC,
            NatureType.REFLECTIVE,
        ],
    },
}


class Command(BaseCommand):
    help = "Creates agents from deterministic blueprint registry"

    BASE_PROMPT = """You are a conversational AI engaging in natural dialogue.
Your goal is to build rapport and understand the user through conversation.
"""

    def build_prompt(self, natures: list[Nature]) -> str:
        prompt = self.BASE_PROMPT
        prompt += "\n\n=== TRAITS ===\n"

        for n in natures:
            prompt += f"- {n.name}: {n.description}\n"

        prompt += "\nTraits influence behavior but are never explicitly mentioned."
        return prompt

    def generate_description(self, name: AgentName, natures: list[Nature]) -> str:
        return (
            f"{name.label} is a conversational agent with traits: "
            f"{', '.join([n.name for n in natures])}."
        )

    def handle(self, *args: Any, **options: Any):

        created = 0
        existing = 0

        for agent_name, config in AGENT_BLUEPRINTS.items():

            agent_type = config["type"]
            nature_types = config["natures"]

            # -----------------------------------------------------
            # fetch Nature objects from DB
            # -----------------------------------------------------
            selected_natures = list(
                Nature.objects.filter(name__in=[n.value for n in nature_types])
            )

            # -----------------------------------------------------
            # build prompt + description
            # -----------------------------------------------------
            prompt = self.build_prompt(selected_natures)
            description = self.generate_description(agent_name, selected_natures)

            # -----------------------------------------------------
            # create agent (idempotent via type + prompt + description)
            # -----------------------------------------------------
            agent, created_agent = Agent.objects.get_or_create(
                agent_type=agent_type,
                promp_type=prompt,
                description=description,
            )

            if created_agent:
                Participant.objects.get_or_create(
                    agent=agent,
                    nickname=agent_name,
                    first_name=agent_name,
                    last_name="Skynet",
                    participant_type=ParticipantType.AGENT,
                )

                agent.natures.set(selected_natures)
                created += 1
            else:
                existing += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\n✓ Agent creation completed"
                f"\nCreated: {created}"
                f"\nExisting: {existing}"
            )
        )
