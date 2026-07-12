# fuel/models.py
from django.db import models
from vehicles.models import Vehicle

class FuelLog(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='fuel_logs')
    fuel_type = models.CharField(max_length=50)
    date = models.DateField()
    liters = models.DecimalField(max_digits=8, decimal_places=2) # in liters
    cost = models.DecimalField(max_digits=10, decimal_places=2) # refueling cost
    odometer = models.PositiveIntegerField() # odometer reading at refueling

    def __str__(self):
        return f"{self.vehicle} - {self.date} (${self.cost})"
