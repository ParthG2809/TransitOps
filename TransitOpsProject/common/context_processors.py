# common/context_processors.py
import datetime
from common.constants import ROLE_ALLOWED_ROUTES
from drivers.models import Driver

def global_context(request):
    # Retrieve current user
    user = request.user
    
    # Handle role
    if user.is_authenticated:
        role = request.session.get('user_role', getattr(user, 'role', 'Driver'))
        user_name = user.full_name or user.username
        user_email = user.email
        user_username = user.username
        user_avatar = user.profile_image
    else:
        role = request.session.get('user_role', 'No Role')
        user_name = request.session.get('user_name', 'Sign In')
        user_email = request.session.get('user_email', '')
        user_username = request.session.get('user_username', '')
        user_avatar = request.session.get('user_avatar', '')

    allowed = ROLE_ALLOWED_ROUTES.get(role, [])

    # Calculate license expiry warnings for warning badge
    expiry_warnings = 0
    try:
        today = datetime.date.today()
        # Find drivers with license expiring in <= 30 days or already expired
        limit_date = today + datetime.timedelta(days=30)
        expiry_warnings = Driver.objects.filter(license_expiry__lte=limit_date).count()
    except Exception:
        pass

    return {
        'current_role': role,
        'user_name': user_name,
        'user_email': user_email,
        'user_username': user_username,
        'user_avatar': user_avatar,
        'theme': request.session.get('theme', 'dark'),
        'allowed_routes': allowed,
        'expiry_warnings': expiry_warnings,
        'all_roles': ['Admin', 'Fleet Manager', 'Driver', 'Safety Officer', 'Financial Analyst']
    }
