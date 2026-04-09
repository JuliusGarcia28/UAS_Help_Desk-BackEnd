from rest_framework import serializers
from .models import Asset
from user.serializers import UserSerializer
from user.models import User

class AssetSerializer(serializers.ModelSerializer):
    responsible = UserSerializer(read_only=True)

    responsible_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='responsible',
        write_only=True,
        required=False,
        allow_null=True
    )

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