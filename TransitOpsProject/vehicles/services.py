# vehicles/services.py
from django.core.exceptions import ValidationError

class VehicleService:
    @staticmethod
    def can_dispatch(vehicle, cargo_weight=0):
        """
        Validates if a vehicle is ready for dispatch.
        """
        if vehicle.status != 'Available':
            raise ValidationError(f"Vehicle {vehicle.registration_number} is currently {vehicle.status} and cannot be dispatched.")
        
        if cargo_weight > vehicle.maximum_load_capacity:
            raise ValidationError(
                f"Cargo weight of {cargo_weight} kg exceeds the vehicle's maximum load capacity of {vehicle.maximum_load_capacity} kg."
            )
        return True

    @staticmethod
    def retire_vehicle(vehicle):
        vehicle.status = 'Retired'
        vehicle.save()
        return vehicle
