# trips/validators.py
from django.core.exceptions import ValidationError

def validate_positive_value(value):
    if value <= 0:
        raise ValidationError("Value must be strictly greater than 0.")
