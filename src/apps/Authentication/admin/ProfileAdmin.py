from django.contrib import admin
from ..models import UserProfile


@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        "nickname",
        "first_name",
        "last_name",
        "gender",
        "custom_gender",
        "birth_date",
    ]
