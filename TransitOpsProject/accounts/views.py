# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.hashers import make_password
from accounts.models import User
from accounts.services import UserService
from common.decorators import login_and_password_required, role_required

def login_view(request):
    if request.user.is_authenticated and not request.session.get('force_password_change'):
        return redirect('dashboard')

    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email', '').strip().lower()
        password = request.POST.get('password', '')

        # Fetch user by username or email
        user = User.objects.filter(username__iexact=username_or_email).first()
        if not user:
            user = User.objects.filter(email__iexact=username_or_email).first()

        if user and user.check_password(password):
            if not user.is_active:
                messages.error(request, "Your account has been deactivated. Please contact your system administrator.")
                return render(request, 'login.html')

            # Log the user in
            auth_login(request, user)
            
            # Set session compat variables
            request.session['user_role'] = user.role
            request.session['user_name'] = user.full_name or user.username
            request.session['user_email'] = user.email
            request.session['user_username'] = user.username

            # Set user avatar
            role = user.role
            if role == 'Admin':
                request.session['user_avatar'] = 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=256'
            elif role == 'Fleet Manager':
                request.session['user_avatar'] = 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&q=80&w=256'
            elif role == 'Driver':
                request.session['user_avatar'] = 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80&w=256'
            elif role == 'Safety Officer':
                request.session['user_avatar'] = 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=256'
            else:
                request.session['user_avatar'] = 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&q=80&w=256'

            if user.needs_password_change:
                request.session['force_password_change'] = True
                messages.warning(request, "First login detected. You must change your temporary password to proceed.")
                return redirect('change_password')

            if 'force_password_change' in request.session:
                del request.session['force_password_change']
            
            messages.success(request, f"Logged in successfully as {user.role}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username/email or password.")

    return render(request, 'login.html')

def logout_view(request):
    auth_logout(request)
    # Clear session role values
    if 'user_role' in request.session:
        del request.session['user_role']
    if 'force_password_change' in request.session:
        del request.session['force_password_change']
    messages.success(request, "Logged out successfully.")
    return redirect('login')

def register_view(request):
    # Registration is blocked for enterprise security
    messages.warning(request, "Registration is closed. Please contact your system administrator to request access.")
    return redirect('login')

def forgot_password_view(request):
    return render(request, 'forgot_password.html')

def otp_verify_view(request):
    return render(request, 'otp_verify.html')

@login_and_password_required
def change_password_view(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not new_password:
            messages.error(request, "Password cannot be empty.")
            return render(request, 'change_password.html')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'change_password.html')

        user = request.user
        user.set_password(new_password)
        user.needs_password_change = False
        user.save()

        # Update session password hash to prevent automatic logout
        update_session_auth_hash(request, user)

        if 'force_password_change' in request.session:
            del request.session['force_password_change']

        messages.success(request, "Password changed successfully! Welcome to your dashboard.")
        return redirect('dashboard')

    return render(request, 'change_password.html')

@login_and_password_required
@role_required(['Admin'])
def users_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        username = request.POST.get('username', '').strip()

        if action == 'create':
            username = request.POST.get('username', '').strip()
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()
            role = request.POST.get('role', '').strip()
            department = request.POST.get('department', '').strip()
            password = request.POST.get('password', '').strip()

            if User.objects.filter(username=username).exists():
                messages.error(request, f"Username '{username}' already exists.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, f"Email '{email}' already exists.")
            else:
                UserService.create_user(
                    username=username,
                    email=email,
                    role=role,
                    full_name=name,
                    temporary_password=password,
                    department=department,
                    phone_number=phone
                )
                messages.success(request, f"User {username} ({role}) created successfully. Temp credentials sent to {email}.")
        
        elif action == 'edit':
            user = User.objects.filter(username=username).first()
            if user:
                user.full_name = request.POST.get('name', '').strip()
                user.email = request.POST.get('email', '').strip()
                user.phone_number = request.POST.get('phone', '').strip()
                user.role = request.POST.get('role', '').strip()
                user.department = request.POST.get('department', '').strip()
                is_active = request.POST.get('is_active')
                if is_active is not None:
                    user.is_active = (is_active == 'True' or is_active is True)
                user.save()
                messages.success(request, f"User details updated for '{username}'.")
            else:
                messages.error(request, "User not found.")

        elif action == 'delete':
            user = User.objects.filter(username=username).first()
            if user:
                user.delete()
                messages.success(request, f"User '{username}' deleted successfully.")
            else:
                messages.error(request, "User not found.")

        elif action == 'reset_password':
            new_password = request.POST.get('new_password', '').strip()
            user = User.objects.filter(username=username).first()
            if user and new_password:
                user.set_password(new_password)
                user.needs_password_change = True
                user.save()
                messages.success(request, f"Password reset for '{username}'. Force change on next login enabled.")
            else:
                messages.error(request, "Could not reset password.")

        elif action == 'toggle_status':
            user = User.objects.filter(username=username).first()
            if user:
                user.is_active = not user.is_active
                user.save()
                status_str = "activated" if user.is_active else "deactivated"
                messages.success(request, f"User '{username}' has been {status_str}.")
            else:
                messages.error(request, "User not found.")

        return redirect('users')

    return render(request, 'user_management.html')
