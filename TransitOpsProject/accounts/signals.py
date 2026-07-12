# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from common.permissions import sync_user_role_groups

@receiver(post_save, sender=User)
def handle_user_save(sender, instance, created, **kwargs):
    """
    Ensure the user belongs to the correct Django Group matching their role.
    """
    sync_user_role_groups(instance)
