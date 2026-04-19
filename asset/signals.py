from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Asset
from .utils import create_asset_snapshot


@receiver(pre_save, sender=Asset)
def save_asset_history(sender, instance, **kwargs):
    if not instance.pk:
        # Es un registro nuevo → no guardar histórico
        return

    try:
        old_asset = Asset.objects.get(pk=instance.pk)
    except Asset.DoesNotExist:
        return

    # Detectar cambios (opcional, pero recomendado)
    fields_to_track = [
        "hostname", "asset_type", "model", "serial_number",
        "operative_system", "cpu", "ram", "ip_address",
        "status", "responsible"
    ]

    changed = False

    for field in fields_to_track:
        if getattr(old_asset, field) != getattr(instance, field):
            changed = True
            break

    if changed:
        create_asset_snapshot(old_asset, reason="update")