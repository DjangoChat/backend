from django.contrib import admin

from ..models import QuotaPlan


@admin.register(QuotaPlan)
class QuotaPlanAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "plan",
        "quota",
        "limit",
    ]
