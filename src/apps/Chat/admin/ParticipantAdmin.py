from django.contrib import admin
from ..models import Participant


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "participaty_type",
        "user",
        "agent",
        "first_name",
        "last_name",
        "nickname",
        "avatar",
        "status",
    ]
