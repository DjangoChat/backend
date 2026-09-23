from django.contrib import admin

from ..models import MessageAnalysis


@admin.register(MessageAnalysis)
class MessageAnalysisAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "message",
        "sentiment",
        "status",
    ]
    readonly_fields = ["embedding"]