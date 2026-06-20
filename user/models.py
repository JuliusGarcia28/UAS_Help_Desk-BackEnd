from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid
import random

ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('technician', 'Technician'),
    ('client', 'Client'),
)

class User(AbstractUser):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    role = models.CharField(
        "Rol",
        max_length=20,
        choices=ROLE_CHOICES
    )

    status = models.SmallIntegerField(
        "Estado",
        default=0
    )

    email_verified = models.BooleanField(
        default=False
    )

    department = models.ForeignKey(
        'Department',
        verbose_name="Departamento",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

class Department(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(
        "Nombre",
        max_length=50
    )

    description = models.CharField(
        "Descripción",
        max_length=100,
        null=True,
        blank=True
    )

    status = models.SmallIntegerField(
        "Estado",
        default=1
    )
    
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="Departamento padre"
    )

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"

    def __str__(self):
        return self.name
    
class AuditLog(models.Model):

    ACTIONS = (
        ("create","Crear"),
        ("update","Actualizar"),
        ("delete","Eliminar"),
        ("login","Login")
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    action = models.CharField(
        max_length=20,
        choices=ACTIONS
    )

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]