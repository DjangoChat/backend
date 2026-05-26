from django.contrib import admin
from ..models import Agent


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "description",
        "agent_type",
        "get_natures",
    ]

    def get_natures(self, obj):
        return [nature.name for nature in obj.natures.all()]
