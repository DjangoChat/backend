from rest_framework import serializers


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
