# drivers/models.py
from django.db import models
from django.conf import settings
from common.constants import DRIVER_STATUS_CHOICES
import datetime

class Driver(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='driver_profile'
    )
    name = models.CharField(max_length=150)
    license_number = models.CharField(max_length=50, unique=True)
    license_category = models.CharField(max_length=50) # e.g. Class A CDL
    license_expiry = models.DateField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField(blank=True)
    photo = models.TextField(blank=True)
    safety_score = models.PositiveIntegerField(default=100)
    status = models.CharField(max_length=30, choices=DRIVER_STATUS_CHOICES, default='Available')
    warning_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_license_expired(self):
        return self.license_expiry < datetime.date.today()

    @property
    def license_status(self):
        today = datetime.date.today()
        if self.license_expiry < today:
            return "Expired"
        elif (self.license_expiry - today).days <= 30:
            return "Expiring Soon"
        return "Valid"

    def __str__(self):
        return self.name
