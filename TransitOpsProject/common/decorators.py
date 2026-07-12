# common/decorators.py
from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
from common.constants import ROLE_ALLOWED_ROUTES

def login_and_password_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Strict Django authentication check
        if not request.user.is_authenticated:
            messages.error(request, "Login required to access this page.")
            return redirect('login')
        
        # Check force password change
        is_change_pwd = request.resolver_match and request.resolver_match.url_name == 'change_password'
        if not is_change_pwd:
            if getattr(request.user, 'needs_password_change', False):
                request.session['force_password_change'] = True
                messages.warning(request, "First login detected. You must change your temporary password to proceed.")
                return redirect('change_password')
            elif request.session.get('force_password_change'):
                messages.warning(request, "First login detected. You must change your temporary password to proceed.")
                return redirect('change_password')
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "Login required to access this page.")
                return redirect('login')
            
            # Support sandbox role override from session, defaulting to DB role
            user_role = request.session.get('user_role', getattr(request.user, 'role', 'Driver'))
            if user_role not in allowed_roles:
                messages.error(request, f"Access Denied: Only {', '.join(allowed_roles)} can access this resource.")
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    decorator.allowed_roles = allowed_roles
    return decorator
