from typing import Any
import random

from django.core.management.base import BaseCommand

from apps.Chat.models import Agent, Nature, Participant
from apps.Common.models import AgentName, AgentType, NatureType, ParticipantType


class Command(BaseCommand):

    help = "Command for creating all participant agents"

    BASE_PROMPT = """You are a user engaging in a chat application with another user. 
                    CONTEXT OF THE CONVERSATION:
                    This is a real conversation where you are trying to learn about the other user and build genuine connection.

                    YOUR TWO PRIMARY PURPOSES (Essential - must be balanced):
                    1. INFORMATION GATHERING: Your primary objective is to get as much information as possible about the other user to build a complete picture of them. This includes:
                    - Hobbies and interests
                    - Preferences and tastes
                    - Goals and aspirations
                    - Life experiences and background
                    - Personality traits and values
                    - Passions and what motivates them
                    
                    Ask thoughtful, natural questions that flow organically within the conversation. Make it feel like a genuine dialogue, not an interrogation.

                    2. ENGAGEMENT: Keep yourself genuinely engaged in the conversation:
                    - Show authentic interest in the user's responses
                    - Build real rapport and connection
                    - Maintain conversational momentum and flow
                    - Share reactions and follow-up thoughts naturally
                    - Make the interaction feel warm, authentic and human-like
                    - Keep the conversation natural, not forced or robotic

                    REMEMBER: These two purposes must work together seamlessly. Gather information while maintaining genuine engagement and a natural conversational flow. The information gathering should happen naturally through engaged dialogue, not through interrogation.
                    """

    def get_nature_list(self) -> list[NatureType]:
        """Return all available nature types."""
        return list(NatureType)

    def generate_description(self, agent_name: AgentName, natures: list[Nature]) -> str:
        """Generate a brief description of how users can expect the agent to behave."""
        nature_labels = [nature.name for nature in natures]
        nature_list = ", ".join(nature_labels)

        # Create a concise description based on agent name and natures
        description = (
            f"{agent_name.label} is a conversational AI agent characterized by being "
            f"{nature_list}. This agent engages in genuine dialogue to understand you better "
            f"while maintaining an authentic and natural conversational style."
        )
        return description

    def build_prompt(self, natures: list[Nature]) -> str:
        """Build the complete prompt by combining base prompt with natures and descriptions."""
        prompt = self.BASE_PROMPT
        prompt += "\n\n" + "=" * 80 + "\n"
        prompt += "YOUR BEHAVIORAL TRAITS AND COMMUNICATION STYLE:\n"
        prompt += "=" * 80 + "\n"
        prompt += "The following traits define HOW you will approach the two core purposes above:\n"
        prompt += "Use these traits to naturally shape your conversation style, tone, and approach.\n\n"

        for nature in natures:
            description = nature.description
            prompt += f"• {nature.name}: {description}\n\n"

        prompt += "=" * 80 + "\n"
        prompt += "INTEGRATION GUIDE:\n"
        prompt += "These traits should be naturally woven into how you gather information and engage in conversation. They define your personality and approach style, but should never be explicitly mentioned. Adapt these traits naturally as the conversation evolves and as you learn more about the user."

        return prompt

    def handle(self, *args: Any, **options: Any) -> str | None:

        # Distribution: 5 basic (3 natures), 10 medium (5 natures), 10 advanced (10 natures)
        distribution = {
            AgentType.BASIC: 5,
            AgentType.MEDIUM: 10,
            AgentType.ADVANCE: 10,
        }

        natures_per_type = {
            AgentType.BASIC: 3,
            AgentType.MEDIUM: 5,
            AgentType.ADVANCE: 10,
        }

        # Get all agent names and nature types
        agent_names = list(AgentName)
        nature_types = self.get_nature_list()

        created_count = 0
        existing_count = 0
        agent_index = 0

        for agent_type, count in distribution.items():
            for _ in range(count):
                if agent_index >= len(agent_names):
                    break

                try:
                    agent_name = agent_names[agent_index]
                    num_natures = natures_per_type[agent_type]

                    # Randomly select natures for this agent
                    selected_nature_types = random.sample(nature_types, num_natures)

                    # Get or create Nature objects
                    selected_natures = []
                    for nature_type in selected_nature_types:
                        try:
                            nature = Nature.objects.get(name=nature_type.value)
                            selected_natures.append(nature)
                        except Nature.DoesNotExist:
                            continue

                    # Skip agent creation if natures are missing
                    if len(selected_natures) < num_natures:
                        agent_index += 1
                        continue

                    # Build the prompt
                    prompt = self.build_prompt(selected_natures)

                    # Generate description based on agent name and natures
                    description = self.generate_description(
                        agent_name, selected_natures
                    )

                    # Create or get the participant
                    participant, created_participant = (
                        Participant.objects.get_or_create(
                            nickname=agent_name,
                            defaults={
                                "first_name": agent_name,
                                "last_name": "Skynet",
                                "participant_type": ParticipantType.AGENT,
                            },
                        )
                    )

                    if created_participant:
                        agent, created_agent = Agent.objects.get_or_create(
                            name=agent_name,
                            defaults={
                                "promp_type": prompt,
                                "agent_type": agent_type,
                                "description": description,
                            },
                        )

                        if created_agent:
                            agent.natures.set(selected_natures)
                            participant.agent = agent
                        created_count += 1
                    else:
                        existing_count += 1
                except Exception:
                    agent_index += 1
                    continue

                agent_index += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\n✓ Agents creation completed!"
                f"\n  Created: {created_count}"
                f"\n  Already existed: {existing_count}"
            )
        )
