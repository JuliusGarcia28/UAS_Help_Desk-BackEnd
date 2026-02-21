from django.db import models
from django.conf import settings
import uuid

class Asset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.CharField(max_length=100)
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=30)
    serial_number = models.CharField(max_length=30)

