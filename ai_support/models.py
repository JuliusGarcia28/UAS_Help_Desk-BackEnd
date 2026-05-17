from django.db import models
from django.conf import settings
from ticket.models import Ticket
from asset.models import Asset

import uuid


class SupportSessionAI(models.Model):

    STATUS_CHOICES = (
        ("active", "Activa"),
        ("solved", "Resuelta"),
        ("escalated", "Escalada"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ai_support_sessions"
    )

    asset = models.ForeignKey(
        Asset,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ai_sessions"
    )

    problem_description = models.TextField()

    ai_response = models.TextField()

    diagnosis = models.TextField(
        null=True,
        blank=True
    )

    detected_priority = models.PositiveSmallIntegerField(default=2)

    category = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    solved = models.BooleanField(default=False)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active"
    )

    ticket = models.OneToOneField(
        Ticket,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ai_support_session"
    )

    created_at = models.DateTimeField(auto_now_add=True)


class SupportMessage(models.Model):

    ROLE_CHOICES = (
        ("user", "Usuario"),
        ("assistant", "IA"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    session = models.ForeignKey(
        SupportSessionAI,
        related_name="messages",
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)