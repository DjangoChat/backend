from django.utils.timezone import now

from rest_framework import serializers

from apps.Authentication.models import UserProfile
from apps.Billing.models import Subscription
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


class UserDataSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    nickname = serializers.CharField()
    group = serializers.CharField(allow_null=True)
    avatar = serializers.ImageField(allow_null=True)


class SubscriptionDataSerializer(serializers.Serializer):
    plan = serializers.CharField()
    status = serializers.CharField()
    current_period_end = serializers.DateTimeField()


class AccessDataSerializer(serializers.Serializer):
    has_access = serializers.BooleanField()
    last_day = serializers.DateTimeField()


class MeSerializerOutput(serializers.Serializer):
    user = UserDataSerializer(allow_null=True)
    subscription = SubscriptionDataSerializer(allow_null=True)
    has_access = AccessDataSerializer()

    def get_user(self, user):
        try:
            profile = user.userprofile
        except UserProfile.DoesNotExist:
            return None

        groups = list(user.groups.values_list("name", flat=True))

        return UserDataSerializer(
            {
                "first_name": profile.first_name,
                "last_name": profile.last_name,
                "nickname": profile.nickname,
                "group": groups[0] if groups else None,
                "avatar": profile.avatar.url if profile.avatar else None,
            }
        ).data

    def get_subscription(self, user):
        subscription = Subscription.objects.filter(user=user).first()

        if not subscription:
            return None

        return SubscriptionDataSerializer(
            {
                "plan": subscription.plan_name,
                "status": subscription.status,
                "current_period_end": subscription.current_period_end,
            }
        ).data

    def get_has_access(self, user):
        subscription = Subscription.objects.filter(user=user).first()

        if not subscription:
            return {
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
                    "has_access": True,
                    "last_day": subscription.current_period_end,
                }
            ).data

        return {
            "has_access": False,
            "last_day": None,
        }
