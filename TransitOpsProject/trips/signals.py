# trips/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from trips.models import Trip

@receiver(post_save, sender=Trip)
def handle_trip_status_change(sender, instance, created, **kwargs):
    """
    Automate vehicle and driver status updates based on the trip's status.
    """
    vehicle = instance.vehicle
    driver = instance.driver

    if instance.status == 'Dispatched':
        vehicle.status = 'On Trip'
        driver.status = 'On Trip'
        vehicle.save()
        driver.save()
    elif instance.status in ['Completed', 'Cancelled']:
        # Only set back to Available if they aren't marked as Retired or Suspended
        if vehicle.status == 'On Trip':
            vehicle.status = 'Available'
        if driver.status == 'On Trip':
            driver.status = 'Available'
            
        # Update vehicle odometer on trip completion
        if instance.status == 'Completed' and instance.actual_distance:
            vehicle.current_odometer += int(instance.actual_distance)
            
        vehicle.save()
        driver.save()
