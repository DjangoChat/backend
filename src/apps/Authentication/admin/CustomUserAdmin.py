from django.contrib import admin

from ..models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "phone",
        "strip_customer_id",
        "verified",
        "is_staff",
        "get_groups",
    ]

    def get_groups(self, obj):
        return ", ".join([g.name for g in obj.groups.all()])

    get_groups.short_description = "Groups"
