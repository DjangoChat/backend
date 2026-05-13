from django.contrib import admin
from ..models import Policy


@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
        "resource_type",
        "action",
        "priority",
        "effect",
    ]
    ordering = ["-priority"]
