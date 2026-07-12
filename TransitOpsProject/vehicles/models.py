# vehicles/models.py
from django.db import models
from common.constants import VEHICLE_STATUS_CHOICES

class Vehicle(models.Model):
    registration_number = models.CharField(max_length=50, unique=True, db_index=True)
    vehicle_name = models.CharField(max_length=100)
    vehicle_model = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=50) # e.g. Cargo Van, Heavy Truck
    fuel_type = models.CharField(max_length=50, blank=True, null=True)
    maximum_load_capacity = models.DecimalField(max_digits=10, decimal_places=2) # in kg
    current_odometer = models.PositiveIntegerField(default=0)
    acquisition_cost = models.DecimalField(max_digits=12, decimal_places=2)
    purchase_date = models.DateField()
    insurance_expiry = models.DateField()
    region = models.CharField(max_length=100)
    status = models.CharField(max_length=30, choices=VEHICLE_STATUS_CHOICES, default='Available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Aliases/compatibility attributes with old session mock structures
    @property
    def name(self):
        return self.vehicle_name

    @property
    def model(self):
        return self.vehicle_model

    @property
    def type(self):
        return self.vehicle_type

    @property
    def capacity(self):
        return f"{self.maximum_load_capacity:,.0f} kg"

    @property
    def odometer(self):
        return self.current_odometer

    @property
    def cost(self):
        return float(self.acquisition_cost)

    def __str__(self):
        return f"{self.vehicle_name} ({self.registration_number})"
