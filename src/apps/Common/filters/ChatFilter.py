import django_filters

from apps.Chat.models import Chat
from apps.Common.models import ChatType


class ChatFilter(django_filters.FilterSet):
    chat_type = django_filters.ChoiceFilter(
        choices=ChatType.choices,
        method="filter_chat_type",
    )

    class Meta:
        model = Chat
        fields = []

    def filter_chat_type(self, queryset, name, value):
        current_user = self.request.user  # type: ignore

        if value == ChatType.AGENT_CHAT:
            return queryset.chats_with_agent(current_user)

        if value == ChatType.USER_CHAT:
            return queryset.chats_without_agent(current_user)

        if value == ChatType.USER_GROUP:
            return queryset.groups_without_agents(current_user)

        if value == ChatType.MIXED_GROUP:
            return queryset.groups_with_agents(current_user)

        return queryset
