from django.contrib import admin

from ..models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "price",
        "status",
        "amount",
        "stripe_subscription_id",
    ]
