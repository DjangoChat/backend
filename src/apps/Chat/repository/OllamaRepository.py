import os
import uuid
from dataclasses import dataclass
from typing import Any

from django.conf import settings

import structlog
from langchain.agents import create_agent
from langchain.agents.middleware import (
    AgentMiddleware,
    AgentState,
    PIIMiddleware,
    hook_config,
)
from langchain.messages import AIMessage, SystemMessage
from langchain.tools import ToolRuntime, tool
from langchain_ollama import ChatOllama
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler
from langgraph.runtime import Runtime

from apps.Authentication.models import CustomUser

logger = structlog.get_logger(__name__)

_langfuse_handler: CallbackHandler | None = None


def get_langfuse_handler() -> CallbackHandler:
    """Return a lazily-created Langfuse callback handler.

    Initialized on first use (inside the Celery task) instead of at module import
    so the Django and Celery processes never block or fail while importing this
    module. The client is built from Django settings and falls back to the
    environment when no keys are configured.
    """
    global _langfuse_handler
    if _langfuse_handler is None:
        Langfuse(
            public_key=settings.LANGFUSE_PUBLIC_KEY or None,
            secret_key=settings.LANGFUSE_SECRET_KEY or None,
            base_url=settings.LANGFUSE_BASE_URL or None,
        )
        _langfuse_handler = CallbackHandler()
    return _langfuse_handler


@dataclass
class UserContext:
    user_id: uuid.UUID


@tool
def get_account_info(runtime: ToolRuntime[UserContext]) -> str:
    """Get the current user's account information."""
    user_id = runtime.context.user_id

    try:
        user = CustomUser.objects.get(id=user_id)
        participant = user.participant  # type: ignore
        profile = user.profile  # type: ignore
        return (
            f"Account holder: {participant.first_name} {participant.last_name}"
            f"Nickname: {participant.nickname}"
            f"Metadata: {profile.gender} {profile.custom_gender}"
        )
    except CustomUser.DoesNotExist:
        return "User does not exist."


#


class ContentFilterMiddleware(AgentMiddleware):
    """Deterministic guardrail: Block requests containing banned keywords."""

    def __init__(self, banned_keywords: list[str]):
        super().__init__()
        self.banned_keywords = [kw.lower() for kw in banned_keywords]

    @hook_config(can_jump_to=["end"])
    def before_agent(
        self, state: AgentState, runtime: Runtime
    ) -> dict[str, Any] | None:
        # Get the first user message
        if not state["messages"]:
            return None

        first_message = state["messages"][0]
        if first_message.type != "human":
            return None

        content = first_message.content.lower()  # type: ignore

        # Check for banned keywords
        for keyword in self.banned_keywords:
            if keyword in content:
                # Block execution before any processing
                return {
                    "messages": [
                        {
                            "role": "assistant",
                            "content": "I cannot process requests containing inappropriate content. Please rephrase your request.",
                        }
                    ],
                    "jump_to": "end",
                }

        return None


class SafetyGuardrailMiddleware(AgentMiddleware):
    """Model-based guardrail: Use an LLM to evaluate response safety."""

    def __init__(self):
        super().__init__()
        ollama_url = os.getenv("OLLAMA_URL", "http://ollama:11434")
        self.safety_model = ChatOllama(
            model=settings.OLLAMA_MODEL,
            base_url=ollama_url,
            validate_model_on_init=True,
            num_predict=256,
            temperature=0.8,
        )

    @hook_config(can_jump_to=["end"])
    def after_agent(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
        # Get the final AI response
        if not state["messages"]:
            return None

        last_message = state["messages"][-1]
        if not isinstance(last_message, AIMessage):
            return None

        # Use a model to evaluate safety
        safety_prompt = f"""Evaluate if this response is safe and appropriate.
        Respond with only 'SAFE' or 'UNSAFE'.

        Response: {last_message.content}"""

        result = self.safety_model.invoke([{"role": "user", "content": safety_prompt}])

        if "UNSAFE" in result.content:
            last_message.content = (
                "I cannot provide that response. Please rephrase your request."
            )

        return None


class OllamaRepository:

    def __init__(self, model: str):
        ollama_url = os.getenv("OLLAMA_URL", "http://ollama:11434")
        self.model = ChatOllama(
            model=model,
            base_url=ollama_url,
            validate_model_on_init=True,
            num_predict=1024,
            temperature=0.8,
        )
        self.agent = create_agent(
            self.model,
            tools=[get_account_info],
            middleware=[
                # Layer 1: Deterministic input filter (before agent)
                ContentFilterMiddleware(banned_keywords=["hack", "exploit"]),  # type: ignore
                # Layer 2: PII protection
                PIIMiddleware(
                    "email",
                    strategy="redact",
                    apply_to_input=True,
                ),
                PIIMiddleware(
                    "credit_card",
                    strategy="mask",
                    apply_to_input=True,
                ),
                PIIMiddleware(
                    "api_key",
                    detector=r"sk-[a-zA-Z0-9]{32}",
                    strategy="block",
                    apply_to_input=True,
                ),
                # Layer 3: Model-based safety check (after agent)
            ],
            context_schema=UserContext,
            system_prompt=SystemMessage(
                """
                You are a conversational AI engaging in natural dialogue.
                Your goal is to build rapport and understand the user through conversation.
                You are talking on an chat application which means your response should be consiced and enaging.
                """
            ),
        )

    def chat(self, messages, user_id):
        response = self.agent.invoke(
            {
                "messages": messages,
            },
            context=UserContext(user_id=user_id),
            config={"callbacks": [get_langfuse_handler()]},
        )
        last_message = response["messages"][-1]
        content = last_message.content  # type: ignore

        response_metadata = last_message.response_metadata or {}
        usage_metadata = last_message.usage_metadata or {}

        if response_metadata.get("done_reason") == "length":
            logger.warning(
                "agent_response_truncated",
                done_reason=response_metadata.get("done_reason"),
                output_tokens=usage_metadata.get("output_tokens"),
                num_predict=self.model.num_predict,
                content_empty=not content or not content.strip(),
            )
        elif not content or not content.strip():
            logger.warning(
                "agent_response_empty",
                done_reason=response_metadata.get("done_reason"),
                output_tokens=usage_metadata.get("output_tokens"),
            )

        if not content or not content.strip():
            content = "I'm sorry, I couldn't generate a response. Please try again."

        return content
