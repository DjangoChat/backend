from rest_framework import serializers


class OnboardingMemberSerializerOutput(serializers.Serializer):
    id_profile = serializers.UUIDField()
    id_participant = serializers.UUIDField()


class OnboardingMemberSerializerInput(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    nickname = serializers.CharField()
    avatar = serializers.ImageField(required=False)
    gender = serializers.CharField()
    custom_gender = serializers.CharField(required=False)
    birth_date = serializers.DateTimeField()
