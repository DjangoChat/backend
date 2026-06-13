from django.db import models
from django.db.models import Count, Q
from django.utils.translation import gettext_lazy as _

from apps.Common.models import (
    ActivatorModelManager,
    ActivatorQuerySet,
    CustomModel,
    ParticipantType,
)


class ChatQuerySet(ActivatorQuerySet):

    def with_participant_counts(self):
        return self.annotate(
            participant_count=Count(
                "participants",
                distinct=True,
            ),
            agent_count=Count(
                "participants",
                filter=Q(
                    chatparticipant__participant__participaty_type=ParticipantType.AGENT
                ),
                distinct=True,
            ),
            user_count=Count(
                "participants",
                filter=Q(
                    chatparticipant__participant__participaty_type=ParticipantType.USER
                ),
                distinct=True,
            ),
        )

    def all_user_chats(self, current_user):
        return self.active().filter(participants__participant__user=current_user)

    def chats_with_agent(self, current_user):
        """
        Chats with exactly two participants
        and at least one agent.
        """
        return (
            self.all_user_chats(current_user)
            .with_participant_counts()
            .filter(
                user_count=1,
                agent_count=1,
            )
        )

    def chats_without_agent(self, current_user):
        """
        Chats with exactly two participants
        none of them are agents.
        """
        return (
            self.all_user_chats(current_user)
            .with_participant_counts()
            .filter(
                user_count=2,
                agent_count=0,
            )
        )

    def groups_without_agents(self, current_user):
        """
        Group chats (>2 participants)
        with zero agents.
        """
        return (
            self.all_user_chats(current_user)
            .with_participant_counts()
            .filter(
                participant_count__gt=2,
                agent_count=0,
            )
        )

    def groups_with_agents(self, current_user):
        return (
            self.all_user_chats(current_user)
            .with_participant_counts()
            .filter(
                participant_count__gt=2,
                agent_count__gt=0,
            )
        )


class ChatManager(ActivatorModelManager):
    def get_queryset(self):
        return ChatQuerySet(
            self.model,
            using=self._db,
        )

    def all_user_chats(self, current_user):
        return self.get_queryset().all_user_chats(current_user)

    def chats_with_agent(self, current_user):
        return self.get_queryset().chats_with_agent(current_user)

    def chats_without_agent(self, current_user):
        return self.get_queryset().chats_without_agent(current_user)

    def groups_without_agents(self, current_user):
        return self.get_queryset().groups_without_agents(current_user)

    def groups_with_agents(self, current_user):
        return self.get_queryset().groups_with_agents(current_user)


# MAYBE: add chat_type (agent_chat, user_chat, group_users, mixed_group)
# and filter that base on type. For the moment, keep single source of truth
class Chat(CustomModel):
    last_message = models.TextField(
        _("Last message send"),
        null=True,
    )
    created_at = models.DateTimeField(
        _("The time the chat was created"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("The time the chat was updated"),
        auto_now=True,
    )

    objects: ChatManager = ChatManager()

    class Meta:
        db_table = "CHAT_CHAT"
        verbose_name = _("Chat")
        verbose_name_plural = _("Chats")
        app_label = "Chat"
        ordering = ["-updated_at"]
