from rest_framework import serializers
from apps.Billing.models import Suscription
from apps.Authentication.models import UserProfile
from apps.Common.models import StatusSuscription
from django.utils.timezone import now


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


class SubscriptionDataSerializer(serializers.Serializer):
    plan = serializers.CharField()
    status = serializers.CharField()
    current_period_end = serializers.DateTimeField()


class AccessDataSerializer(serializers.Serializer):
    has_access = serializers.BooleanField()
    last_day = serializers.DateTimeField()


class MeResponseSerializer(serializers.Serializer):
    user = UserDataSerializer(allow_null=True)
    subscription = SubscriptionDataSerializer(allow_null=True)
    has_access = AccessDataSerializer(allow_null=True)

    @staticmethod
    def create_me_response_data(user):

        try:
            profile = user.userprofile
            groups = list(user.groups.values_list("name", flat=True))
            group_name = groups[0] if groups else None

            user_data = {
                "first_name": profile.first_name,
                "last_name": profile.last_name,
                "nickname": profile.nickname,
                "group": group_name,
            }
        except UserProfile.DoesNotExist:
            user_data = None

        subscription = Suscription.objects.filter(user=user).first()

        suscription_data = None
        has_access = None

        if subscription:
            suscription_data = {
                "plan": subscription.plan_name,
                "status": subscription.status,
                "current_period_end": subscription.current_period_end,
            }

            if subscription.status is StatusSuscription.ACTIVE:
                has_access = {
                    "has_access": True,
                    "last_day": Suscription.current_period_end,
                }
            elif (
                subscription.status is StatusSuscription.CANCELED
                and subscription.current_period_end
                and subscription.current_period_end > now()
            ):
                has_access = {
                    "has_access": True,
                    "last_day": Suscription.current_period_end,
                }

        return {
            "user": user_data,
            "subscription": suscription_data,
            "has_access": has_access,
        }
