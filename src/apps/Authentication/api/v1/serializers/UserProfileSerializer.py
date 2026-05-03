from rest_framework import serializers

from apps.Authentication.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "nickname",
            "first_name",
            "last_name",
            "gender",
            "custom_gender",
            "birth_date",
            "avatar",
        ]
        read_only_fields = ["id"]
