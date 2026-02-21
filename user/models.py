from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid
import random

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=15)
    status = models.SmallIntegerField(default=0)

    def is_active_user(self):
        return self.status == 1

    def deactivate(self):
        self.status = 0
        self.save()

class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    status = models.SmallIntegerField(default=1)