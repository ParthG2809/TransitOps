# trips/models.py
from django.db import models
from django.conf import settings
from common.constants import TRIP_STATUS_CHOICES
from vehicles.models import Vehicle
from drivers.models import Driver

class Trip(models.Model):
    trip_number = models.CharField(max_length=50, unique=True, db_index=True)
    source = models.CharField(max_length=150)
    destination = models.CharField(max_length=150)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='trips')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='trips')
    cargo_weight = models.DecimalField(max_digits=10, decimal_places=2) # in kg
    planned_distance = models.DecimalField(max_digits=8, decimal_places=2) # in miles
    actual_distance = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    fuel_used = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True) # in gallons
    trip_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    dispatch_time = models.DateTimeField(null=True, blank=True)
    completion_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=TRIP_STATUS_CHOICES, default='Draft')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_trips'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.trip_number}: {self.source} -> {self.destination}"
