# trips/services.py
from django.core.exceptions import ValidationError
from django.utils import timezone
from vehicles.services import VehicleService
from drivers.services import DriverService

class TripService:
    @staticmethod
    def dispatch_trip(trip):
        """
        Validates vehicle/driver and marks trip as Dispatched.
        """
        if trip.status != 'Draft':
            raise ValidationError(f"Only Draft trips can be dispatched. Current status is {trip.status}.")

        # Check vehicle capacity and status
        VehicleService.can_dispatch(trip.vehicle, trip.cargo_weight)
        # Check driver availability
        DriverService.can_dispatch(trip.driver)

        trip.status = 'Dispatched'
        trip.dispatch_time = timezone.now()
        trip.save()
        return trip

    @staticmethod
    def complete_trip(trip, actual_distance, fuel_used):
        """
        Completes the trip and sets distances and fuel logs.
        """
        if trip.status != 'Dispatched':
            raise ValidationError(f"Only Dispatched trips can be completed. Current status is {trip.status}.")

        trip.actual_distance = actual_distance
        trip.fuel_used = fuel_used
        trip.status = 'Completed'
        trip.completion_time = timezone.now()
        trip.save()

        # Create fuel expense log automatically if fuel_used is recorded
        if fuel_used and fuel_used > 0:
            from expenses.models import Expense
            import datetime
            Expense.objects.create(
                vehicle=trip.vehicle,
                expense_type='Fuel',
                amount=float(fuel_used) * 90.0,  # ₹90 per liter
                description=f"Automated fuel cost for completed trip {trip.trip_number}",
                expense_date=datetime.date.today()
            )

        return trip

    @staticmethod
    def cancel_trip(trip):
        """
        Cancels the trip.
        """
        if trip.status not in ['Draft', 'Dispatched']:
            raise ValidationError(f"Completed or already Cancelled trips cannot be cancelled.")

        trip.status = 'Cancelled'
        trip.save()
        return trip
