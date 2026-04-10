from django.contrib import admin
from ..models import Quota


@admin.register(Quota)
class QuotaAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "plan",
        "code",
        "limit",
    ]
