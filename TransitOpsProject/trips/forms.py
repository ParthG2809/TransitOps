# trips/forms.py
from django import forms
from trips.models import Trip
from trips.validators import validate_positive_value

class TripForm(forms.ModelForm):
    cargo_weight = forms.DecimalField(validators=[validate_positive_value])
    planned_distance = forms.DecimalField(validators=[validate_positive_value])
    trip_revenue = forms.DecimalField(validators=[validate_positive_value])

    class Meta:
        model = Trip
        fields = [
            'trip_number', 'source', 'destination', 'vehicle', 'driver', 
            'cargo_weight', 'planned_distance', 'trip_revenue', 'status'
        ]
