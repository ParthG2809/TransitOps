import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TransitOpsProject.settings')
django.setup()

from django.core.management import call_command
from accounts.models import User
from accounts.services import UserService
from drivers.models import Driver

def seed():
    # 1. Run migrations first
    print("Running migrations...")
    call_command('migrate')

    # 2. Seed Users
    users_to_create = [
        {
            'username': 'Parth',
            'email': 'parthgoyal0289@gmail.com',
            'role': 'Admin',
            'full_name': 'Parth Goyal',
            'password': 'Parth@123',
            'department': 'Logistics',
            'phone_number': '9876543200'
        },
        {
            'username': 'parth_driver',
            'email': 'parthgoyal2809@gmail.com',
            'role': 'Driver',
            'full_name': 'Parth Goyal (Driver)',
            'password': 'Parth@123',
            'department': 'Logistics',
            'phone_number': '9876543201'
        },
        {
            'username': 'parth_safety',
            'email': 'chronix2809@gmail.com',
            'role': 'Safety Officer',
            'full_name': 'Parth (Safety Officer)',
            'password': 'Parth@123',
            'department': 'Safety & Compliance',
            'phone_number': '9876543202'
        },
        {
            'username': 'parth_fleet',
            'email': 'parth28@gmail.com',
            'role': 'Fleet Manager',
            'full_name': 'Parth (Fleet Manager)',
            'password': 'Parth@123',
            'department': 'Logistics',
            'phone_number': '9876543203'
        },
        {
            'username': 'parth_analyst',
            'email': 'parth0928@gmail.com',
            'role': 'Financial Analyst',
            'full_name': 'Parth (Financial Analyst)',
            'password': 'Parth@123',
            'department': 'Finance',
            'phone_number': '9876543204'
        }
    ]

    for u in users_to_create:
        user = User.objects.filter(email=u['email']).first()
        if not user:
            user = User.objects.filter(username=u['username']).first()
        
        if not user:
            print(f"Creating user {u['username']} ({u['role']})...")
            user = UserService.create_user(
                username=u['username'],
                email=u['email'],
                role=u['role'],
                full_name=u['full_name'],
                temporary_password=u['password'],
                department=u['department'],
                phone_number=u['phone_number']
            )
            # Remove needs_password_change for default seeded users so they can log in directly
            user.needs_password_change = False
            user.save()
            
            # If driver, also seed a Driver profile
            if u['role'] == 'Driver':
                Driver.objects.get_or_create(
                    user=user,
                    defaults={
                        'name': u['full_name'],
                        'phone': u['phone_number'],
                        'license_number': 'DL-1420240098765',
                        'license_category': 'Heavy Motor Vehicle (HMV)',
                        'license_expiry': '2030-12-31',
                        'safety_score': 95,
                        'status': 'Available',
                        'email': u['email']
                    }
                )
        else:
            print(f"User {u['username']} already exists.")

    print("Database seeding completed successfully!")

if __name__ == '__main__':
    seed()
