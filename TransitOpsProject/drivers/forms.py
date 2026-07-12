# drivers/forms.py
from django import forms
from drivers.models import Driver
from drivers.validators import validate_phone_number

class DriverForm(forms.ModelForm):
    phone = forms.CharField(validators=[validate_phone_number])

    class Meta:
        model = Driver
        fields = [
            'name', 'license_number', 'license_category', 'license_expiry', 
            'phone', 'email', 'address', 'photo', 'safety_score', 'status'
        ]
        # Include optional User binding if needed
