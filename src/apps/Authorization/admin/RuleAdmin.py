from django.contrib import admin
from ..models import Rule


@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = [
        "policy",
        "rule_type",
        "attribute_name",
        "operator",
        "value",
    ]
