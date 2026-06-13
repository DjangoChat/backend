from django.contrib import admin

from ..models import Nature


@admin.register(Nature)
class NatureAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "description",
    ]
