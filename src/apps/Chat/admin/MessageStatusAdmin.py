from django.contrib import admin
from ..models import MessageStatus


@admin.register(MessageStatus)
class MessageStatusAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "participant",
        "message",
        "status",
        "upload_at",
    ]
    ordering = ["-upload_at"]
