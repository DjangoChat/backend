from django.contrib import admin

from ..models import ChatParticipant


@admin.register(ChatParticipant)
class ChatParticipantAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "chat",
        "participant",
        "joined_at",
        "is_muted",
        "is_admin",
    ]
    ordering = ["-joined_at"]
