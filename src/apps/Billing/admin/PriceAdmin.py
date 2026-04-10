from django.contrib import admin
from ..models import Price


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "plan__name",
        "period__name",
        "currency__code",
        "amount",
        "stripe_price_id",
    ]
