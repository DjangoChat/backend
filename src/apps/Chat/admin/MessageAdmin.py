from django.contrib import admin
from ..models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "chat",
        "sender",
        "content",
        "created_at",
    ]
    ordering = ["-created_at"]
