from django.contrib import admin
from ..models import Suscription


@admin.register(Suscription)
class SuscriptionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "price",
        "status",
        "amount",
        "strip_sucription_id",
    ]
