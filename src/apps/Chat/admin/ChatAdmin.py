from django.contrib import admin

from ..models import Chat


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "photo",
        "created_at",
    ]
    ordering = ["-created_at"]
