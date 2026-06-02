from rest_framework import serializers
from apps.Chat.models import Nature


class DropdownNatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Nature
        fields = [
            "id",
            "name",
        ]


class ChipNatureSerializer(serializers.ListSerializer):
    child = serializers.CharField()

    def to_representation(self, data):
        return list(data.values_list("name", flat=True))
