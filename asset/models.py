from django.db import models
from django.conf import settings
import uuid


ASSET_STATUS = (
    (1, "Activo"),
    (0, "Inactivo"),
    (2, "En mantenimiento"),
)


class Asset(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    hostname = models.CharField(max_length=100)

    asset_type = models.CharField("Tipo de equipo", max_length=30)

    model = models.CharField("Modelo", max_length=50)

    serial_number = models.CharField("Número de serie", max_length=50, unique=True)

    operative_system = models.CharField(
        "Sistema operativo",
        max_length=50,
        null=True,
        blank=True
    )

    cpu = models.CharField(
        "Procesador",
        max_length=150,
        null=True,
        blank=True
    )

    ram = models.IntegerField(
        "Memoria RAM (GB)",
        null=True,
        blank=True
    )

    ip_address = models.GenericIPAddressField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    last_service = models.DateTimeField(null=True, blank=True)

    status = models.SmallIntegerField(
        choices=ASSET_STATUS,
        default=1
    )

    responsible = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assets'
    )

    class Meta:
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"

    def __str__(self):
        return f"{self.hostname} - {self.serial_number}"
    
class AssetHistory(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    asset_id = models.UUIDField()  # referencia del asset original

    # =========================
    # Snapshot del asset
    # =========================
    hostname = models.CharField(max_length=100)
    asset_type = models.CharField(max_length=30)
    model = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=50)

    operative_system = models.CharField(max_length=50, null=True, blank=True)
    cpu = models.CharField(max_length=150, null=True, blank=True)
    ram = models.IntegerField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    status = models.SmallIntegerField()
    created_at = models.DateTimeField()
    last_service = models.DateTimeField(null=True, blank=True)

    # =========================
    # Snapshot del usuario relacionado
    # =========================
    user_email = models.EmailField(null=True, blank=True)
    user_id = models.UUIDField(null=True, blank=True)

    department_name = models.CharField(max_length=50, null=True, blank=True)
    department_id = models.UUIDField(null=True, blank=True)

    # =========================
    # metadata del historial
    # =========================
    snapshot_date = models.DateTimeField(auto_now_add=True)
    change_reason = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Historial de Equipo"
        verbose_name_plural = "Historial de Equipos"
        ordering = ["-snapshot_date"]