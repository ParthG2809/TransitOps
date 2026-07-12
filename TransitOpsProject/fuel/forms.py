# fuel/forms.py
from django import forms
from fuel.models import FuelLog

class FuelLogForm(forms.ModelForm):
    class Meta:
        model = FuelLog
        fields = ['vehicle', 'fuel_type', 'date', 'liters', 'cost', 'odometer']
