# drivers/services.py
from django.core.exceptions import ValidationError
import datetime

class DriverService:
    @staticmethod
    def can_dispatch(driver):
        """
        Checks if driver is available and holds a valid (unexpired) license.
        """
        if driver.status != 'Available':
            raise ValidationError(f"Driver {driver.name} is currently {driver.status} and cannot be dispatched.")
        
        if driver.license_expiry < datetime.date.today():
            raise ValidationError(f"Driver {driver.name} has an expired license ({driver.license_expiry}) and cannot be dispatched.")
            
        return True

    @staticmethod
    def update_safety_score(driver, delta):
        driver.safety_score = max(0, min(100, driver.safety_score + delta))
        driver.save()
        return driver
