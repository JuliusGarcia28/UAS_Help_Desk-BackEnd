from rest_framework import serializers
from .models import Asset


class AssetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Asset
        fields = "__all__"


class AgentAssetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Asset
        fields = [
            "hostname",
            "asset_type",
            "model",
            "serial_number",
            "operative_system",
            "cpu",
            "ram",
            "ip_address",
        ]
        extra_kwargs = {
            "serial_number": {"required": True}
        }