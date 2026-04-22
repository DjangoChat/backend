from rest_framework import serializers

from apps.Billing.models import Price


class PriceSerializer(serializers.ModelSerializer):
    plan = serializers.SerializerMethodField()
    period = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()

    def get_plan(self, obj):
        return obj.plan.name

    def get_period(self, obj):
        return obj.period.name

    def get_currency(self, obj):
        return obj.currency.simbol

    class Meta:
        model = Price
        fields = [
            "id",
            "plan",
            "period",
            "currency",
            "amount",
            "stripe_price_id",
        ]
        read_only_fields = [
            "id",
            "plan",
            "period",
            "currency",
            "amount",
            "stripe_price_id",
        ]
