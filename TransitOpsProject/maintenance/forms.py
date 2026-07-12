# maintenance/forms.py
from django import forms
from maintenance.models import Maintenance

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = ['vehicle', 'maintenance_type', 'description', 'technician', 'cost', 'start_date', 'end_date', 'status']
