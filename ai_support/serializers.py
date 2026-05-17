from rest_framework import serializers

from .models import (
    SupportSessionAI,
    SupportMessage
)


class SupportMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupportMessage
        fields = "__all__"


class SupportSessionSerializer(serializers.ModelSerializer):

    messages = SupportMessageSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = SupportSessionAI
        fields = "__all__"