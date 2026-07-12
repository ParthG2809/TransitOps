# vehicles/forms.py
from django import forms
from vehicles.models import Vehicle
from vehicles.validators import validate_license_plate

class VehicleForm(forms.ModelForm):
    registration_number = forms.CharField(validators=[validate_license_plate])

    class Meta:
        model = Vehicle
        fields = [
            'registration_number', 'vehicle_name', 'vehicle_model', 'vehicle_type', 
            'fuel_type', 'maximum_load_capacity', 'current_odometer', 'acquisition_cost', 
            'purchase_date', 'insurance_expiry', 'region', 'status'
        ]
