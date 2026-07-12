# settings_app/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from common.decorators import login_and_password_required
from common.constants import ROLE_ALLOWED_ROUTES

User = get_user_model()

@login_and_password_required
def settings_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_profile':
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip()
            avatar = request.POST.get('avatar', '').strip()

            if not email:
                messages.error(request, "Email address is required.")
                return redirect('settings')

            # Update request.user
            user = request.user
            user.full_name = name
            user.email = email
            if avatar:
                user.profile_image = avatar
            user.save()

            # Sync with session variables
            request.session['user_name'] = name or user.username
            request.session['user_email'] = email
            if avatar:
                request.session['user_avatar'] = avatar

            messages.success(request, "Profile updated successfully.")
            return redirect('settings')

    # Prefill context variables
    user = request.user
    role = request.session.get('user_role', getattr(user, 'role', 'Driver'))
    
    context = {
        'user_name': user.full_name or user.username,
        'user_email': user.email,
        'user_username': user.username,
        'user_avatar': user.profile_image,
        'current_role': role,
        'all_roles': ['Admin', 'Fleet Manager', 'Driver', 'Safety Officer', 'Financial Analyst']
    }
    return render(request, 'settings.html', context)

@login_and_password_required
def switch_role_view(request):
    if request.method == 'POST':
        # Block actual Drivers and Safety Officers from switching sandbox roles
        if request.user.role in ['Driver', 'Safety Officer']:
            messages.error(request, "Access denied. Drivers and Safety Officers are not authorized to switch sandbox roles.")
            return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

        role = request.POST.get('role')
        if role in ['Admin', 'Fleet Manager', 'Driver', 'Safety Officer', 'Financial Analyst']:
            request.session['user_role'] = role
            # If authenticated user, also temporarily override their role in the session
            # This is extremely useful for sandbox evaluation as requested
            messages.success(request, f"Switched active workspace role to: {role}")
        
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

@login_and_password_required
def toggle_theme_view(request):
    current_theme = request.session.get('theme', 'dark')
    new_theme = 'light' if current_theme == 'dark' else 'dark'
    request.session['theme'] = new_theme
    
    # Also save theme to user if authenticated
    # Just update in session is enough, but can store in profile if desired
    pass

    messages.info(request, f"Theme toggled to {new_theme} mode.")
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))
