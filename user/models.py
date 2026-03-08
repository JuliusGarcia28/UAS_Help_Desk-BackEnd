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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    status = models.SmallIntegerField(default=0)

    department = models.ForeignKey(
        'Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )

    def is_active_user(self):
        return self.status == 1

    def deactivate(self):
        self.status = 0
        self.save()

class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=True, blank=True)
    status = models.SmallIntegerField(default=1)