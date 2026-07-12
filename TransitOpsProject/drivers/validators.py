# drivers/validators.py
import re
from django.core.exceptions import ValidationError

def validate_phone_number(value):
    pattern = r'^\+?[1-9]\d{1,14}$'
    if not re.match(pattern, value):
        raise ValidationError("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
