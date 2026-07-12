# vehicles/validators.py
import re
from django.core.exceptions import ValidationError

def validate_license_plate(value):
    """
    Ensure the license plate registration has standard alphanumeric format.
    """
    pattern = r'^[A-Z0-9\- ]{5,15}$'
    if not re.match(pattern, value, re.IGNORECASE):
        raise ValidationError("Registration number must be 5-15 alphanumeric characters, hyphens or spaces.")
