from django.db import models
from django.conf import settings
from asset.models import Asset
import uuid

STATUS_CHOICES = (
    (1, "Abierto"),
    (2, "En proceso"),
    (3, "Resuelto"),
)

SOURCE_CHOICES = (
    ("manual", "Manual"),
    ("ai", "IA"),
)

CATEGORY_CHOICES = (
    ("Hardware", "Hardware"),
    ("Software", "Software"),
    ("Network", "Network"),
    ("Access", "Access"),
    ("Other", "Other"),
)


class Ticket(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    description = models.TextField()

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default="Other"
    )

    diagnosis = models.TextField(
        blank=True,
        null=True
    )

    resolution = models.TextField(
        blank=True,
        null=True
    )

    priority = models.PositiveSmallIntegerField(
        default=2
    )

    status = models.SmallIntegerField(
        default=1,
        choices=STATUS_CHOICES
    )

    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        default="manual"
    )

    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="tickets_creados",
        on_delete=models.CASCADE
    )

    technician = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="tickets_asignados",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    asset = models.ForeignKey(
        Asset,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    finished_at = models.DateTimeField(
        null=True,
        blank=True
    )

    resolution_time = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.id}"
    
class TicketHistory(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    ticket = models.ForeignKey(
        Ticket,
        related_name="history",
        on_delete=models.CASCADE
    )

    status = models.SmallIntegerField()

    priority = models.PositiveSmallIntegerField()

    category = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    diagnosis = models.TextField(
        blank=True,
        null=True
    )

    technician_id = models.UUIDField(
        null=True,
        blank=True
    )

    technician_email = models.EmailField(
        null=True,
        blank=True
    )

    changed_by_id = models.UUIDField(
        null=True,
        blank=True
    )

    changed_by_email = models.EmailField(
        null=True,
        blank=True
    )

    change_reason = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    change_date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-change_date"]