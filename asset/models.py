from django.db import models
from django.conf import settings
import uuid

class Asset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset_type = models.CharField(max_length=30)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=30)
    serial_number = models.CharField(max_length=30)
    operative_system = models.CharField(max_length=30, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_service = models.DateTimeField(null=True, blank=True)
    status = models.SmallIntegerField(default=1)

    responsible = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assets'
    )

    def __str__(self):
        return f"{self.asset_type} - {self.serial_number}"