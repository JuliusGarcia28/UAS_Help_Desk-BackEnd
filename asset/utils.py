from .models import AssetHistory

# Guardar snapshot del asset para el historico    
from asset.models import AssetHistory


def create_asset_snapshot(asset, reason="update"):
    user = asset.responsible

    AssetHistory.objects.create(
        asset_id=asset.id,

        hostname=asset.hostname,
        asset_type=asset.asset_type,
        model=asset.model,
        serial_number=asset.serial_number,
        operative_system=asset.operative_system,
        cpu=asset.cpu,
        ram=asset.ram,
        ip_address=asset.ip_address,

        status=asset.status,
        created_at=asset.created_at,
        last_service=asset.last_service,

        user_email=user.email if user else None,
        user_id=user.id if user else None,

        department_name=user.department.name if user and user.department else None,
        department_id=user.department.id if user and user.department else None,

        change_reason=reason
    )