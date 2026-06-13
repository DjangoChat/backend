from django.contrib import admin

from ..models import Agent


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "agent_type",
        "get_natures",
        "promp_type",
    ]

    def get_natures(self, obj):
        return [nature.name for nature in obj.natures.all()]
