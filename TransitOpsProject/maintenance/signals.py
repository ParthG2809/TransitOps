# maintenance/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from maintenance.models import Maintenance

@receiver(post_save, sender=Maintenance)
def handle_maintenance_status_change(sender, instance, created, **kwargs):
    """
    Automate vehicle status updates based on maintenance.
    """
    vehicle = instance.vehicle

    if instance.status == 'Open':
        vehicle.status = 'In Shop'
        vehicle.save()
    elif instance.status == 'Completed':
        if vehicle.status == 'In Shop':
            vehicle.status = 'Available'
            vehicle.save()
