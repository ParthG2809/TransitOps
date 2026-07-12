# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from common.constants import ROLE_CHOICES

class User(AbstractUser):
    full_name = models.CharField(max_length=150, blank=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='Driver')
    needs_password_change = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=20, blank=True)
    profile_image = models.TextField(
        default='https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=256'
    )
    department = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        # Always split full_name to first_name and last_name when full_name is provided
        if self.full_name:
            parts = self.full_name.split(' ', 1)
            self.first_name = parts[0]
            if len(parts) > 1:
                self.last_name = parts[1]
            else:
                self.last_name = ""
        elif self.first_name:
            self.full_name = f"{self.first_name} {self.last_name}".strip()
        super().save(*args, **kwargs)
