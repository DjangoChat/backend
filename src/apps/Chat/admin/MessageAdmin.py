from django.contrib import admin
from ..models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "chat",
        "participant",
        "content",
        "sent_at",
    ]
    ordering = ["-sent_at"]
