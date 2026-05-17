from django.db import models
from django.conf import settings
import uuid

STATUS_CHOICES = (
    (1, "Abierto"),
    (2, "En proceso"),
    (3, "Cerrado"),
)

class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()
    priority = models.PositiveSmallIntegerField(default=2)
    finished_at = models.DateTimeField(null=True, blank=True)
    resolution_time = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    status = models.SmallIntegerField(default=1, choices=STATUS_CHOICES)
    
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tickets_creados'
    )

class Ticket_Detail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    note = models.CharField(max_length=100)
    diagnostic = models.CharField(max_length=100, null=True)

    ticket = models.ForeignKey(
        'Ticket',
        on_delete=models.CASCADE,
        related_name='detalles'
    )

    tecnico = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets_asignados'
    )
    
class TicketHistory(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    ticket_id = models.UUIDField()

    # estado del ticket en ese momento
    status = models.SmallIntegerField()

    # prioridad
    priority = models.PositiveSmallIntegerField()

    # quién hizo el cambio
    changed_by_id = models.UUIDField(null=True, blank=True)
    changed_by_email = models.EmailField(null=True, blank=True)

    # metadata
    change_date = models.DateTimeField(auto_now_add=True)
    change_reason = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ["-change_date"]
    
class support_session_ai(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    problem_description = models.CharField(max_length=100)
    ai_response = models.CharField(max_length=100, null=True)
    suggestions = models.CharField(max_length=100, null=True)   
    user_attemp = models.BooleanField(default=False)
    solved = models.BooleanField(default=False)
    start_at = models.DateTimeField(auto_now_add=True) 

    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ai_sessions'
    )

    ticket = models.OneToOneField(
        'Ticket',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='ai_session'
    )