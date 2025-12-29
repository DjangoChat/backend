from rest_framework import serializers
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
    )
    password = serializers.CharField(
        write_only=True,
    )

    def validate(self, data):
        user = authenticate(**data)

        if user:
            return user

        raise serializers.ValidationError("Incorrect Credentials")
