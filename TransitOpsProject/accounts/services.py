# accounts/services.py
import logging
from django.core.mail import send_mail
from django.conf import settings
from accounts.models import User
from common.permissions import sync_user_role_groups

logger = logging.getLogger(__name__)

class UserService:
    @staticmethod
    def create_user(username, email, role, full_name, temporary_password, department="", phone_number=""):
        """
        Creates a User in the database, sets their role, adds them to Django Groups, 
        and dispatches temporary credentials to their email via SMTP.
        """
        user = User.objects.create_user(
            username=username,
            email=email,
            role=role,
            full_name=full_name,
            password=temporary_password,
            department=department,
            phone_number=phone_number,
            needs_password_change=True
        )
        
        # Sync with Django group
        sync_user_role_groups(user)
        
        # Send credentials via SMTP
        subject = "TransitOps ERP - Temporary Account Credentials"
        message = (
            f"Hello {full_name},\n\n"
            f"An enterprise account has been created for you on TransitOps.\n\n"
            f"Your temporary credentials are as follows:\n"
            f"Username: {username}\n"
            f"Temporary Password: {temporary_password}\n"
            f"Role: {role}\n\n"
            f"Please log in at http://localhost:8000/login/ and change your password immediately.\n\n"
            f"Regards,\n"
            f"TransitOps System Admin"
        )
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL or 'parthgoyal0289@gmail.com',
                [email],
                fail_silently=False,
            )
        except Exception as e:
            # Catch gracefully to avoid blocking user creation if network/SMTP issue occurs during testing
            logger.error(f"Failed to send email to {email}: {e}")
            print(f"Warning: Credentials email not sent: {e}")
            
        return user
