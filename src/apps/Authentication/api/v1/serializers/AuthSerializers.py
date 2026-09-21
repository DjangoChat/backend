from django.utils.timezone import now

from rest_framework import serializers

from apps.Billing.models import Subscription
from apps.Chat.models import Participant
from apps.Common.models import StatusSuscription


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
    )
    password = serializers.CharField(
        write_only=True,
    )


class LoginResponseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    profile = serializers.BooleanField()

    @staticmethod
    def create_login_response_data(user):
        from apps.Authentication.models import UserProfile

        return {
            "email": user.email,
            "profile": UserProfile.objects.filter(user=user).exists(),
        }


class ParticipantDataSerializer(serializers.Serializer):
    required = serializers.BooleanField(default=True)
    id = serializers.UUIDField(default=True)
    group = serializers.CharField(allow_null=True)


class SubscriptionDataSerializer(serializers.Serializer):
    required = serializers.BooleanField(default=True)
    plan = serializers.CharField()
    status = serializers.CharField()
    current_period_end = serializers.DateTimeField(allow_null=True)


class AccessDataSerializer(serializers.Serializer):
    required = serializers.BooleanField(default=True)
    has_access = serializers.BooleanField()
    last_day = serializers.DateTimeField(allow_null=True)


class MeSerializerOutput(serializers.Serializer):
    user = serializers.SerializerMethodField()
    subscription = serializers.SerializerMethodField()
    has_access = serializers.SerializerMethodField()

    def get_user(self, user):
        try:
            participant = user.participant
        except Participant.DoesNotExist:
            return ParticipantDataSerializer(
                {
                    "required": True,
                    "id": None,
                    "group": None,
                }
            ).data

        groups = list(user.groups.values_list("name", flat=True))

        return ParticipantDataSerializer(
            {
                "required": False,
                "id": participant.id,
                "group": groups[0] if groups else None,
            }
        ).data

    def get_subscription(self, user):
        subscription = Subscription.objects.filter(user=user).first()

        if not subscription:
            return SubscriptionDataSerializer(
                {
                    "required": True,
                    "plan": "",
                    "status": "",
                    "current_period_end": None,
                }
            ).data

        return SubscriptionDataSerializer(
            {
                "required": False,
                "plan": subscription.plan_name,
                "status": subscription.status,
                "current_period_end": subscription.current_period_end,
            }
        ).data

    def get_has_access(self, user):
        subscription = Subscription.objects.filter(user=user).first()

        if not subscription:
            return {
                "required": True,
                "has_access": False,
                "last_day": None,
            }

        if subscription.status == StatusSuscription.ACTIVE or (
            subscription.status == StatusSuscription.CANCELED
            and subscription.current_period_end
            and subscription.current_period_end > now()
        ):
            return AccessDataSerializer(
                {
                    "required": False,
                    "has_access": True,
                    "last_day": subscription.current_period_end,
                }
            ).data

        return {
            "required": False,
            "has_access": False,
            "last_day": None,
        }
