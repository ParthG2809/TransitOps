# maintenance/models.py
from django.db import models
from django.conf import settings
from common.constants import MAINTENANCE_STATUS_CHOICES, MAINTENANCE_TYPE_CHOICES
from vehicles.models import Vehicle

class Maintenance(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenance_logs')
    maintenance_type = models.CharField(max_length=30, choices=MAINTENANCE_TYPE_CHOICES, default='Routine')
    description = models.TextField()
    technician = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=MAINTENANCE_STATUS_CHOICES, default='Open')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_maintenances'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vehicle} - {self.maintenance_type} ({self.status})"
