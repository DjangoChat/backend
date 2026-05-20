from django.contrib import admin
from ..models import Chat


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "created_at",
        "updated_at",
    ]
    ordering = ["-created_at"]
