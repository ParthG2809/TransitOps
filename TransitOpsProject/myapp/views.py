import json
import hashlib
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from datetime import datetime, timedelta

def mock_hash(pw):
    return hashlib.sha256(pw.encode('utf-8')).hexdigest()

# Helper to initialize session-based mock database
def init_mock_db(session):
    # Re-initialize if the registered_users list only contains the old mock format
    if 'initialized' not in session or 'registered_users' not in session or len(session.get('registered_users', [])) <= 1 or 'password' not in session.get('registered_users', [{}])[0]:
        session['initialized'] = True
        session['theme'] = 'dark' # Default theme is dark
        session['registered_users'] = [
            {
                'name': 'Alex Mercer',
                'username': 'admin',
                'email': 'admin@transitops.com',
                'password': mock_hash('admin123'),
                'role': 'Admin',
                'department': 'Operations',
                'phone': '+1 (555) 0199',
                'is_active': True,
                'needs_password_change': False
            },
            {
                'name': 'Marcus Vance',
                'username': 'fleet_mgr',
                'email': 'fleet@transitops.com',
                'password': mock_hash('temp123'),
                'role': 'Fleet Manager',
                'department': 'Logistics',
                'phone': '+1 (555) 0288',
                'is_active': True,
                'needs_password_change': True
            },
            {
                'name': 'Elena Rostova',
                'username': 'driver_user',
                'email': 'driver@transitops.com',
                'password': mock_hash('driver123'),
                'role': 'Driver',
                'department': 'Logistics',
                'phone': '+1 (555) 0377',
                'is_active': True,
                'needs_password_change': False
            },
            {
                'name': 'David Chen',
                'username': 'safety_user',
                'email': 'safety@transitops.com',
                'password': mock_hash('safety123'),
                'role': 'Safety Officer',
                'department': 'Safety & Compliance',
                'phone': '+1 (555) 0466',
                'is_active': True,
                'needs_password_change': False
            },
            {
                'name': 'Sarah Jenkins',
                'username': 'finance_user',
                'email': 'finance@transitops.com',
                'password': mock_hash('finance123'),
                'role': 'Financial Analyst',
                'department': 'Finance',
                'phone': '+1 (555) 0555',
                'is_active': True,
                'needs_password_change': False
            }
        ]
        
        # 1. Vehicles Registry
        session['vehicles'] = [
            {
                'id': 1,
                'registration_number': 'TX-9088-GP',
                'name': 'Scania R450 Heavy Hauler',
                'model': 'R450 - 2022',
                'type': 'Heavy Duty Truck',
                'capacity': '32,000 kg',
                'cost': 145000,
                'odometer': 124500,
                'status': 'Available'
            },
            {
                'id': 2,
                'registration_number': 'CA-8822-LP',
                'name': 'Volvo FH16 Flatbed',
                'model': 'FH16 - 2021',
                'type': 'Flatbed Truck',
                'capacity': '26,000 kg',
                'cost': 132000,
                'odometer': 98200,
                'status': 'On Trip'
            },
            {
                'id': 3,
                'registration_number': 'NY-4401-TR',
                'name': 'Mercedes-Benz Actros',
                'model': 'Actros 2646 - 2023',
                'type': 'Semi-Trailer',
                'capacity': '40,000 kg',
                'cost': 165000,
                'odometer': 42100,
                'status': 'In Shop'
            },
            {
                'id': 4,
                'registration_number': 'FL-7712-MK',
                'name': 'Isuzu NPR Box Truck',
                'model': 'NPR Cargo - 2020',
                'type': 'Box Truck',
                'capacity': '8,500 kg',
                'cost': 75000,
                'odometer': 185200,
                'status': 'Available'
            },
            {
                'id': 5,
                'registration_number': 'TX-3398-MN',
                'name': 'Ford F-550 Service Rig',
                'model': 'F-550 - 2019',
                'type': 'Utility Vehicle',
                'capacity': '4,500 kg',
                'cost': 62000,
                'odometer': 243100,
                'status': 'Retired'
            },
            {
                'id': 6,
                'registration_number': 'NV-6652-PL',
                'name': 'Kenworth T680 Sleeper',
                'model': 'T680 - 2022',
                'type': 'Heavy Duty Truck',
                'capacity': '36,000 kg',
                'cost': 158000,
                'odometer': 112000,
                'status': 'On Trip'
            }
        ]
        
        # 2. Drivers Registry
        session['drivers'] = [
            {
                'id': 1,
                'name': 'Marcus Vance',
                'license_number': 'DL-9082319A',
                'license_category': 'Class A CDL',
                'license_expiry': '2026-09-15',
                'phone': '+1 (555) 234-5678',
                'safety_score': 94,
                'status': 'On Duty'
            },
            {
                'id': 2,
                'name': 'Sarah Jenkins',
                'license_number': 'DL-8827361B',
                'license_category': 'Class A CDL',
                'license_expiry': '2026-07-28', # Near expiry (warning!)
                'phone': '+1 (555) 345-6789',
                'safety_score': 98,
                'status': 'On Duty'
            },
            {
                'id': 3,
                'name': 'Roberto Gomez',
                'license_number': 'DL-4410293X',
                'license_category': 'Class B CDL',
                'license_expiry': '2027-02-14',
                'phone': '+1 (555) 456-7890',
                'safety_score': 81,
                'status': 'Active'
            },
            {
                'id': 4,
                'name': 'David Chen',
                'license_number': 'DL-7738291M',
                'license_category': 'Class A CDL',
                'license_expiry': '2026-05-10', # Expired!
                'phone': '+1 (555) 567-8901',
                'safety_score': 72,
                'status': 'Suspended'
            },
            {
                'id': 5,
                'name': 'Elena Rostova',
                'license_number': 'DL-5529104Y',
                'license_category': 'Class A CDL',
                'license_expiry': '2028-11-30',
                'phone': '+1 (555) 678-9012',
                'safety_score': 99,
                'status': 'Active'
            }
        ]
        
        # 3. Trips Log
        session['trips'] = [
            {
                'id': 1,
                'source': 'Houston Hub',
                'destination': 'Dallas Distribution',
                'vehicle': 'Volvo FH16 Flatbed (CA-8822-LP)',
                'driver': 'Marcus Vance',
                'cargo_weight': 22000,
                'distance': 240.5,
                'status': 'Dispatched',
                'dispatched_time': '2026-07-12 06:30',
                'completed_time': ''
            },
            {
                'id': 2,
                'source': 'El Paso Depot',
                'destination': 'Austin Warehouse',
                'vehicle': 'Kenworth T680 Sleeper (NV-6652-PL)',
                'driver': 'Sarah Jenkins',
                'cargo_weight': 31500,
                'distance': 576.2,
                'status': 'Dispatched',
                'dispatched_time': '2026-07-11 22:15',
                'completed_time': ''
            },
            {
                'id': 3,
                'source': 'Chicago Logistics Center',
                'destination': 'Indianapolis Cargo Hub',
                'vehicle': 'Scania R450 Heavy Hauler (TX-9088-GP)',
                'driver': 'Elena Rostova',
                'cargo_weight': 28000,
                'distance': 185.0,
                'status': 'Completed',
                'dispatched_time': '2026-07-11 08:00',
                'completed_time': '2026-07-11 11:30'
            },
            {
                'id': 4,
                'source': 'Phoenix Depot',
                'destination': 'Los Angeles Port',
                'vehicle': 'Mercedes-Benz Actros (NY-4401-TR)',
                'driver': 'Roberto Gomez',
                'cargo_weight': 38000,
                'distance': 372.8,
                'status': 'Cancelled',
                'dispatched_time': '2026-07-10 14:00',
                'completed_time': ''
            }
        ]
        
        # 4. Maintenance Logs
        session['maintenance'] = [
            {
                'id': 1,
                'vehicle': 'Mercedes-Benz Actros (NY-4401-TR)',
                'type': 'Repair',
                'description': 'Transmission fluid leak and clutch calibration.',
                'cost': 2450.00,
                'date': '2026-07-10',
                'status': 'Open'
            },
            {
                'id': 2,
                'vehicle': 'Scania R450 Heavy Hauler (TX-9088-GP)',
                'type': 'Routine',
                'description': '120k mile engine service, oil and air filter replacement.',
                'cost': 850.00,
                'date': '2026-07-08',
                'status': 'Completed'
            },
            {
                'id': 3,
                'vehicle': 'Isuzu NPR Box Truck (FL-7712-MK)',
                'type': 'Inspection',
                'description': 'Brake pad inspection and tire rotation.',
                'cost': 320.00,
                'date': '2026-07-05',
                'status': 'Completed'
            },
            {
                'id': 4,
                'vehicle': 'Ford F-550 Service Rig (TX-3398-MN)',
                'type': 'Repair',
                'description': 'Suspension strut replacement and front wheel alignment.',
                'cost': 1200.00,
                'date': '2026-07-12',
                'status': 'Open'
            }
        ]
        
        # 5. Fuel & Expense Logs
        session['fuel_logs'] = [
            {
                'id': 1,
                'vehicle': 'Volvo FH16 Flatbed (CA-8822-LP)',
                'liters': 320.5,
                'cost': 580.90,
                'odometer': 98200,
                'date': '2026-07-11'
            },
            {
                'id': 2,
                'vehicle': 'Kenworth T680 Sleeper (NV-6652-PL)',
                'liters': 410.0,
                'cost': 742.10,
                'odometer': 112000,
                'date': '2026-07-11'
            },
            {
                'id': 3,
                'vehicle': 'Scania R450 Heavy Hauler (TX-9088-GP)',
                'liters': 295.8,
                'cost': 535.40,
                'odometer': 124500,
                'date': '2026-07-10'
            }
        ]
        
        session['expense_logs'] = [
            {
                'id': 1,
                'vehicle': 'Mercedes-Benz Actros (NY-4401-TR)',
                'category': 'Parts',
                'cost': 1450.00,
                'date': '2026-07-10',
                'description': 'Clutch cylinder assembly part replacement'
            },
            {
                'id': 2,
                'vehicle': 'Volvo FH16 Flatbed (CA-8822-LP)',
                'category': 'Toll',
                'cost': 85.00,
                'date': '2026-07-11',
                'description': 'Interstate toll fees for Houston-Dallas run'
            },
            {
                'id': 3,
                'vehicle': 'Kenworth T680 Sleeper (NV-6652-PL)',
                'category': 'Insurance',
                'cost': 450.00,
                'date': '2026-07-01',
                'description': 'Monthly fleet insurance allocation'
            }
        ]
        
        # 6. Role Permissions Matrix
        session['role_matrix'] = {
            'Admin': ['dashboard', 'fleet', 'drivers', 'trips', 'maintenance', 'expenses', 'analytics', 'settings', 'users'],
            'Fleet Manager': ['dashboard', 'fleet', 'maintenance', 'analytics'],
            'Driver': ['dashboard', 'trips'],
            'Safety Officer': ['dashboard', 'drivers', 'settings'],
            'Financial Analyst': ['dashboard', 'expenses', 'analytics']
        }

def get_allowed_routes(role):
    # Map roles to their permitted navbar/sidebar tabs
    matrix = {
        'Admin': ['dashboard', 'fleet', 'drivers', 'trips', 'maintenance', 'expenses', 'analytics', 'settings', 'users'],
        'Fleet Manager': ['dashboard', 'fleet', 'maintenance', 'analytics'],
        'Driver': ['dashboard', 'trips'],
        'Safety Officer': ['dashboard', 'drivers', 'settings'],
        'Financial Analyst': ['dashboard', 'expenses', 'analytics']
    }
    return matrix.get(role, [])

# Context processor style helper
def get_global_context(request):
    init_mock_db(request.session)
    role = request.session.get('user_role')
    allowed = get_allowed_routes(role) if role else []
    
    # Calculate global indicators, warnings
    drivers = request.session.get('drivers', [])
    expiry_warnings = 0
    today = datetime.today().date()
    for d in drivers:
        try:
            exp_date = datetime.strptime(d['license_expiry'], '%Y-%m-%d').date()
            if exp_date <= today + timedelta(days=30):
                expiry_warnings += 1
        except:
            pass

    return {
        'current_role': role or 'No Role',
        'user_name': request.session.get('user_name', 'Sign In'),
        'user_avatar': request.session.get('user_avatar', ''),
        'theme': request.session.get('theme', 'dark'),
        'allowed_routes': allowed,
        'expiry_warnings': expiry_warnings,
        'all_roles': ['Admin', 'Fleet Manager', 'Driver', 'Safety Officer', 'Financial Analyst']
    }

# --- VIEW CONTROLLERS ---

def login_view(request):
    init_mock_db(request.session)
    
    # If already logged in and not forced to change password, redirect to dashboard
    if request.session.get('user_role') and not request.session.get('force_password_change'):
        return redirect('dashboard')

    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_email', '').strip().lower()
        password = request.POST.get('password', '')
        
        registered_users = request.session.get('registered_users', [])
        
        user = None
        for u in registered_users:
            if u.get('username', '').lower() == username_or_email or u.get('email', '').lower() == username_or_email:
                user = u
                break
                
        if user:
            if user.get('password') == mock_hash(password):
                if not user.get('is_active', True):
                    messages.error(request, "Your account has been deactivated. Please contact your system administrator.")
                    return render(request, 'login.html', {'theme': request.session.get('theme', 'dark')})
                
                # Set session details
                request.session['user_role'] = user['role']
                request.session['user_name'] = user['name']
                request.session['user_email'] = user['email']
                request.session['user_username'] = user['username']
                
                role = user['role']
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
                
                # Verify first login password reset requirement
                if user.get('needs_password_change', False):
                    request.session['force_password_change'] = True
                    messages.warning(request, "First login detected. You must change your temporary password to proceed.")
                    return redirect('change_password')
                
                if 'force_password_change' in request.session:
                    del request.session['force_password_change']
                messages.success(request, f"Logged in successfully as {user['role']}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username/email or password.")
        else:
            messages.error(request, "Invalid username/email or password.")
            
    context = {
        'theme': request.session.get('theme', 'dark'),
        'all_roles': ['Admin', 'Fleet Manager', 'Driver', 'Safety Officer', 'Financial Analyst']
    }
    return render(request, 'login.html', context)

def logout_view(request):
    for key in ['user_role', 'user_name', 'user_avatar', 'user_email', 'user_username', 'force_password_change']:
        if key in request.session:
            del request.session[key]
    messages.info(request, "You have been logged out.")
    return redirect('login')

def register_view(request):
    return redirect('login')

def otp_verify_view(request):
    return redirect('login')

def forgot_password_view(request):
    init_mock_db(request.session)
    context = {
        'theme': request.session.get('theme', 'dark'),
    }
    return render(request, 'forgot_password.html', context)

def change_password_view(request):
    init_mock_db(request.session)
    if not request.session.get('user_username'):
        messages.error(request, "Please log in first.")
        return redirect('login')
        
    if request.method == 'POST':
        new_pw = request.POST.get('new_password', '')
        confirm_pw = request.POST.get('confirm_password', '')
        
        if new_pw != confirm_pw:
            messages.error(request, "Passwords do not match!")
        elif len(new_pw) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
        else:
            username = request.session['user_username']
            users = request.session.get('registered_users', [])
            updated = False
            for u in users:
                if u['username'] == username:
                    u['password'] = mock_hash(new_pw)
                    u['needs_password_change'] = False
                    updated = True
                    break
            if updated:
                request.session['registered_users'] = users
                if 'force_password_change' in request.session:
                    del request.session['force_password_change']
                messages.success(request, "Your password has been successfully updated.")
                return redirect('dashboard')
            else:
                messages.error(request, "User session error.")
                
    return render(request, 'change_password.html', {'theme': request.session.get('theme', 'dark')})

def users_view(request):
    init_mock_db(request.session)
    
    if not request.session.get('user_role'):
        messages.error(request, "Login required to access this page.")
        return redirect('login')
        
    # RBAC check
    if request.session.get('user_role') != 'Admin':
        messages.error(request, "Access Denied: Only Administrators can access User Management.")
        return redirect('dashboard')
        
    if request.session.get('force_password_change'):
        messages.warning(request, "Please change your temporary password first.")
        return redirect('change_password')
        
    registered_users = request.session.get('registered_users', [])
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            name = request.POST.get('name', '').strip()
            username = request.POST.get('username', '').strip().lower()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()
            role = request.POST.get('role', 'Driver')
            department = request.POST.get('department', '').strip()
            password = request.POST.get('password', '')
            confirm_password = request.POST.get('confirm_password', '')
            is_active = request.POST.get('is_active') == 'True' or request.POST.get('is_active') == 'on'
            
            if any(u['username'].lower() == username for u in registered_users):
                messages.error(request, f"Username '{username}' already exists. Please choose a unique username.")
            elif password != confirm_password:
                messages.error(request, "Passwords do not match!")
            elif len(password) < 8:
                messages.error(request, "Password must be at least 8 characters long.")
            else:
                new_user = {
                    'name': name,
                    'username': username,
                    'email': email,
                    'phone': phone,
                    'role': role,
                    'department': department,
                    'password': mock_hash(password),
                    'is_active': is_active,
                    'needs_password_change': True
                }
                registered_users.append(new_user)
                request.session['registered_users'] = registered_users
                messages.success(request, f"User account for {name} (@{username}) created successfully.")
                
        elif action == 'edit':
            username = request.POST.get('username', '').strip().lower()
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()
            role = request.POST.get('role')
            department = request.POST.get('department', '').strip()
            is_active = request.POST.get('is_active') == 'True' or request.POST.get('is_active') == 'on'
            
            updated = False
            for u in registered_users:
                if u['username'].lower() == username:
                    u['name'] = name
                    u['email'] = email
                    u['phone'] = phone
                    u['role'] = role
                    u['department'] = department
                    u['is_active'] = is_active
                    updated = True
                    break
            if updated:
                request.session['registered_users'] = registered_users
                messages.success(request, f"User profile for @{username} updated successfully.")
            else:
                messages.error(request, "User not found.")
                
        elif action == 'toggle_status':
            username = request.POST.get('username', '').strip().lower()
            updated = False
            for u in registered_users:
                if u['username'].lower() == username:
                    u['is_active'] = not u.get('is_active', True)
                    updated = True
                    status_str = "activated" if u['is_active'] else "deactivated"
                    messages.success(request, f"User @{username} successfully {status_str}.")
                    break
            if updated:
                request.session['registered_users'] = registered_users
            else:
                messages.error(request, "User not found.")
                
        elif action == 'reset_password':
            username = request.POST.get('username', '').strip().lower()
            password = request.POST.get('password', '')
            confirm_password = request.POST.get('confirm_password', '')
            
            if password != confirm_password:
                messages.error(request, "Passwords do not match!")
            elif len(password) < 8:
                messages.error(request, "Password must be at least 8 characters long.")
            else:
                updated = False
                for u in registered_users:
                    if u['username'].lower() == username:
                        u['password'] = mock_hash(password)
                        u['needs_password_change'] = True
                        updated = True
                        break
                if updated:
                    request.session['registered_users'] = registered_users
                    messages.success(request, f"Temporary password reset for @{username} successfully. Password change forced on next login.")
                else:
                    messages.error(request, "User not found.")
                    
        elif action == 'delete':
            username = request.POST.get('username', '').strip().lower()
            initial_count = len(registered_users)
            registered_users = [u for u in registered_users if u['username'].lower() != username]
            if len(registered_users) < initial_count:
                request.session['registered_users'] = registered_users
                messages.success(request, f"User @{username} has been permanently deleted.")
            else:
                messages.error(request, "User not found.")
                
        return redirect('users')

    q = request.GET.get('q', '').strip().lower()
    role_filter = request.GET.get('role', '').strip()
    status_filter = request.GET.get('status', '').strip()
    
    filtered_users = []
    for u in registered_users:
        if q and not (q in u['name'].lower() or q in u['username'].lower() or q in u['email'].lower()):
            continue
        if role_filter and u['role'] != role_filter:
            continue
        if status_filter:
            is_act = u.get('is_active', True)
            if status_filter == 'active' and not is_act:
                continue
            if status_filter == 'inactive' and is_act:
                continue
        filtered_users.append(u)
        
    g_ctx = get_global_context(request)
    context = {
        **g_ctx,
        'users': filtered_users,
        'q': q,
        'role_filter': role_filter,
        'status_filter': status_filter,
    }
    return render(request, 'user_management.html', context)

def switch_role_view(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        if role in ['Admin', 'Fleet Manager', 'Driver', 'Safety Officer', 'Financial Analyst']:
            request.session['user_role'] = role
            request.session['user_name'] = f"{role} User" if role != 'Admin' else 'Alex Mercer'
            messages.success(request, f"Switched active workspace role to {role}.")
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

def toggle_theme_view(request):
    current = request.session.get('theme', 'dark')
    new_theme = 'light' if current == 'dark' else 'dark'
    request.session['theme'] = new_theme
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

def login_and_password_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_role'):
            messages.error(request, "Login required to access this page.")
            return redirect('login')
        if request.session.get('force_password_change'):
            messages.warning(request, "Please change your temporary password first.")
            return redirect('change_password')
        return view_func(request, *args, **kwargs)
    return wrapper

# 1. DASHBOARD
@login_and_password_required
def dashboard_view(request):
    g_context = get_global_context(request)
    
    # Check authorization
    if 'dashboard' not in g_context['allowed_routes']:
        messages.error(request, "Access denied to Dashboard.")
        return redirect('login')
        
    if request.session.get('force_password_change'):
        messages.warning(request, "Please change your temporary password first.")
        return redirect('change_password')
        
    vehicles = request.session.get('vehicles', [])
    drivers = request.session.get('drivers', [])
    trips = request.session.get('trips', [])
    maintenance = request.session.get('maintenance', [])
    
    # Calculate dynamic stats
    active_vehicles = sum(1 for v in vehicles if v['status'] in ['Available', 'On Trip'])
    available_vehicles = sum(1 for v in vehicles if v['status'] == 'Available')
    vehicles_in_maintenance = sum(1 for v in vehicles if v['status'] == 'In Shop')
    drivers_on_duty = sum(1 for d in drivers if d['status'] == 'On Duty')
    pending_trips = sum(1 for t in trips if t['status'] == 'Draft')
    active_trips = sum(1 for t in trips if t['status'] == 'Dispatched')
    
    # Total operational cost calculations
    maint_cost = sum(m['cost'] for m in maintenance)
    fuel_cost = sum(f['cost'] for f in request.session.get('fuel_logs', []))
    expense_cost = sum(e['cost'] for e in request.session.get('expense_logs', []))
    total_cost = maint_cost + fuel_cost + expense_cost
    
    # Fleet utilization percentage
    total_v = len(vehicles)
    fleet_utilization = int((active_trips / total_v) * 100) if total_v > 0 else 0
    
    # Filter handling for dashboard elements
    sel_vehicle_type = request.GET.get('vehicle_type', '')
    sel_status = request.GET.get('status', '')
    
    filtered_vehicles = vehicles
    if sel_vehicle_type:
        filtered_vehicles = [v for v in filtered_vehicles if v['type'] == sel_vehicle_type]
    if sel_status:
        filtered_vehicles = [v for v in filtered_vehicles if v['status'] == sel_status]
        
    # Get recent trips
    recent_trips = sorted(trips, key=lambda x: x['id'], reverse=True)[:5]
    
    # Charts data mock
    charts = {
        'fleet_utilization_labels': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
        'fleet_utilization_data': [65, 78, 82, fleet_utilization],
        
        'vehicle_status_labels': ['Available', 'On Trip', 'In Shop', 'Retired'],
        'vehicle_status_data': [
            sum(1 for v in vehicles if v['status'] == 'Available'),
            sum(1 for v in vehicles if v['status'] == 'On Trip'),
            sum(1 for v in vehicles if v['status'] == 'In Shop'),
            sum(1 for v in vehicles if v['status'] == 'Retired')
        ],
        
        'trip_status_labels': ['Draft', 'Dispatched', 'Completed', 'Cancelled'],
        'trip_status_data': [
            sum(1 for t in trips if t['status'] == 'Draft'),
            sum(1 for t in trips if t['status'] == 'Dispatched'),
            sum(1 for t in trips if t['status'] == 'Completed'),
            sum(1 for t in trips if t['status'] == 'Cancelled')
        ],
        
        'monthly_expenses_labels': ['May', 'Jun', 'Jul (Curr)'],
        'monthly_expenses_data': [45000, 52000, int(total_cost)]
    }

    context = {
        **g_context,
        'active_vehicles': active_vehicles,
        'available_vehicles': available_vehicles,
        'vehicles_in_maintenance': vehicles_in_maintenance,
        'drivers_on_duty': drivers_on_duty,
        'pending_trips': pending_trips,
        'active_trips': active_trips,
        'fleet_utilization': fleet_utilization,
        'operational_cost': total_cost,
        'recent_trips': recent_trips,
        'vehicles': filtered_vehicles,
        'charts': charts,
        'charts_json': json.dumps(charts),
        'vehicle_types': sorted(list(set(v['type'] for v in vehicles))),
        'statuses': ['Available', 'On Trip', 'In Shop', 'Retired'],
        'sel_vehicle_type': sel_vehicle_type,
        'sel_status': sel_status
    }
    return render(request, 'dashboard.html', context)

# 2. VEHICLE REGISTRY
@login_and_password_required
def vehicles_view(request):
    g_context = get_global_context(request)
    if 'fleet' not in g_context['allowed_routes']:
        messages.error(request, "Access denied to Fleet Management.")
        return redirect('dashboard')
        
    vehicles = request.session.get('vehicles', [])
    
    # Create Vehicle Form Submission
    if request.method == 'POST' and 'action' in request.POST:
        action = request.POST.get('action')
        
        if action == 'create':
            new_id = max([v['id'] for v in vehicles]) + 1 if vehicles else 1
            new_vehicle = {
                'id': new_id,
                'registration_number': request.POST.get('registration_number'),
                'name': request.POST.get('name'),
                'model': request.POST.get('model'),
                'type': request.POST.get('type'),
                'capacity': request.POST.get('capacity'),
                'cost': float(request.POST.get('cost') or 0),
                'odometer': int(request.POST.get('odometer') or 0),
                'status': request.POST.get('status', 'Available')
            }
            vehicles.append(new_vehicle)
            request.session['vehicles'] = vehicles
            messages.success(request, f"Vehicle {new_vehicle['registration_number']} added successfully!")
            return redirect('vehicles')
            
        elif action == 'edit':
            v_id = int(request.POST.get('id'))
            for v in vehicles:
                if v['id'] == v_id:
                    v['registration_number'] = request.POST.get('registration_number')
                    v['name'] = request.POST.get('name')
                    v['model'] = request.POST.get('model')
                    v['type'] = request.POST.get('type')
                    v['capacity'] = request.POST.get('capacity')
                    v['cost'] = float(request.POST.get('cost') or 0)
                    v['odometer'] = int(request.POST.get('odometer') or 0)
                    v['status'] = request.POST.get('status')
                    break
            request.session['vehicles'] = vehicles
            messages.success(request, "Vehicle updated successfully!")
            return redirect('vehicles')
            
        elif action == 'delete':
            v_id = int(request.POST.get('id'))
            vehicles = [v for v in vehicles if v['id'] != v_id]
            request.session['vehicles'] = vehicles
            messages.warning(request, "Vehicle removed from registry.")
            return redirect('vehicles')

    # View Mode: table or card
    view_mode = request.GET.get('view', 'table')
    
    # Search and Filters
    q = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '')
    
    filtered_vehicles = vehicles
    if q:
        filtered_vehicles = [
            v for v in filtered_vehicles
            if q.lower() in v['registration_number'].lower() or q.lower() in v['name'].lower() or q.lower() in v['type'].lower()
        ]
    if status_filter:
        filtered_vehicles = [v for v in filtered_vehicles if v['status'] == status_filter]
        
    context = {
        **g_context,
        'vehicles': filtered_vehicles,
        'view_mode': view_mode,
        'q': q,
        'status_filter': status_filter,
        'statuses': ['Available', 'On Trip', 'In Shop', 'Retired']
    }
    return render(request, 'vehicles.html', context)

# 3. DRIVER MANAGEMENT
@login_and_password_required
def drivers_view(request):
    g_context = get_global_context(request)
    if 'drivers' not in g_context['allowed_routes']:
        messages.error(request, "Access denied to Driver Management.")
        return redirect('dashboard')
        
    drivers = request.session.get('drivers', [])
    
    if request.method == 'POST' and 'action' in request.POST:
        action = request.POST.get('action')
        
        if action == 'create':
            new_id = max([d['id'] for d in drivers]) + 1 if drivers else 1
            new_driver = {
                'id': new_id,
                'name': request.POST.get('name'),
                'license_number': request.POST.get('license_number'),
                'license_category': request.POST.get('license_category'),
                'license_expiry': request.POST.get('license_expiry'),
                'phone': request.POST.get('phone'),
                'safety_score': int(request.POST.get('safety_score') or 95),
                'status': request.POST.get('status', 'Active')
            }
            drivers.append(new_driver)
            request.session['drivers'] = drivers
            messages.success(request, f"Driver {new_driver['name']} added successfully!")
            return redirect('drivers')
            
        elif action == 'edit':
            d_id = int(request.POST.get('id'))
            for d in drivers:
                if d['id'] == d_id:
                    d['name'] = request.POST.get('name')
                    d['license_number'] = request.POST.get('license_number')
                    d['license_category'] = request.POST.get('license_category')
                    d['license_expiry'] = request.POST.get('license_expiry')
                    d['phone'] = request.POST.get('phone')
                    d['safety_score'] = int(request.POST.get('safety_score') or 95)
                    d['status'] = request.POST.get('status')
                    break
            request.session['drivers'] = drivers
            messages.success(request, "Driver details updated.")
            return redirect('drivers')
            
        elif action == 'delete':
            d_id = int(request.POST.get('id'))
            drivers = [d for d in drivers if d['id'] != d_id]
            request.session['drivers'] = drivers
            messages.warning(request, "Driver profile deleted.")
            return redirect('drivers')
            
        elif action == 'suspend':
            d_id = int(request.POST.get('id'))
            for d in drivers:
                if d['id'] == d_id:
                    d['status'] = 'Suspended'
                    break
            request.session['drivers'] = drivers
            messages.warning(request, "Driver has been suspended.")
            return redirect('drivers')

    view_mode = request.GET.get('view', 'table')
    q = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '')
    
    filtered_drivers = drivers
    if q:
        filtered_drivers = [
            d for d in filtered_drivers
            if q.lower() in d['name'].lower() or q.lower() in d['license_number'].lower()
        ]
    if status_filter:
        filtered_drivers = [d for d in filtered_drivers if d['status'] == status_filter]
        
    context = {
        **g_context,
        'drivers': filtered_drivers,
        'view_mode': view_mode,
        'q': q,
        'status_filter': status_filter,
        'statuses': ['Active', 'On Duty', 'Suspended']
    }
    return render(request, 'drivers.html', context)

# 4. TRIP MANAGEMENT
@login_and_password_required
def trips_view(request):
    g_context = get_global_context(request)
    if 'trips' not in g_context['allowed_routes']:
        messages.error(request, "Access denied to Trip Dispatcher.")
        return redirect('dashboard')
        
    trips = request.session.get('trips', [])
    vehicles = request.session.get('vehicles', [])
    drivers = request.session.get('drivers', [])
    
    if request.method == 'POST' and 'action' in request.POST:
        action = request.POST.get('action')
        
        if action == 'dispatch':
            new_id = max([t['id'] for t in trips]) + 1 if trips else 1
            new_trip = {
                'id': new_id,
                'source': request.POST.get('source'),
                'destination': request.POST.get('destination'),
                'vehicle': request.POST.get('vehicle'),
                'driver': request.POST.get('driver'),
                'cargo_weight': float(request.POST.get('cargo_weight') or 0),
                'distance': float(request.POST.get('distance') or 0),
                'status': 'Dispatched',
                'dispatched_time': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'completed_time': ''
            }
            # Update vehicle status to On Trip
            for v in vehicles:
                if v['registration_number'] in new_trip['vehicle'] or v['name'] in new_trip['vehicle']:
                    v['status'] = 'On Trip'
            # Update driver status to On Duty
            for d in drivers:
                if d['name'] == new_trip['driver']:
                    d['status'] = 'On Duty'
                    
            trips.append(new_trip)
            request.session['trips'] = trips
            request.session['vehicles'] = vehicles
            request.session['drivers'] = drivers
            messages.success(request, f"Trip #{new_id} dispatched successfully to {new_trip['driver']}!")
            return redirect('trips')
            
        elif action == 'complete':
            trip_id = int(request.POST.get('id'))
            for t in trips:
                if t['id'] == trip_id:
                    t['status'] = 'Completed'
                    t['completed_time'] = datetime.now().strftime('%Y-%m-%d %H:%M')
                    # Make vehicle available again
                    for v in vehicles:
                        if v['registration_number'] in t['vehicle'] or v['name'] in t['vehicle']:
                            v['status'] = 'Available'
                    # Make driver active again
                    for d in drivers:
                        if d['name'] == t['driver']:
                            d['status'] = 'Active'
                    break
            request.session['trips'] = trips
            request.session['vehicles'] = vehicles
            request.session['drivers'] = drivers
            messages.success(request, "Trip marked as completed.")
            return redirect('trips')
            
        elif action == 'cancel':
            trip_id = int(request.POST.get('id'))
            for t in trips:
                if t['id'] == trip_id:
                    t['status'] = 'Cancelled'
                    # Reset statuses
                    for v in vehicles:
                        if v['registration_number'] in t['vehicle'] or v['name'] in t['vehicle']:
                            v['status'] = 'Available'
                    for d in drivers:
                        if d['name'] == t['driver']:
                            d['status'] = 'Active'
                    break
            request.session['trips'] = trips
            request.session['vehicles'] = vehicles
            request.session['drivers'] = drivers
            messages.warning(request, "Trip has been cancelled.")
            return redirect('trips')
            
    q = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '')
    
    filtered_trips = trips
    if q:
        filtered_trips = [
            t for t in filtered_trips
            if q.lower() in t['source'].lower() or q.lower() in t['destination'].lower() or q.lower() in t['driver'].lower()
        ]
    if status_filter:
        filtered_trips = [t for t in filtered_trips if t['status'] == status_filter]
        
    context = {
        **g_context,
        'trips': filtered_trips,
        'available_vehicles': [v for v in vehicles if v['status'] == 'Available'],
        'available_drivers': [d for d in drivers if d['status'] == 'Active'],
        'q': q,
        'status_filter': status_filter
    }
    return render(request, 'trips.html', context)

# 5. MAINTENANCE
@login_and_password_required
def maintenance_view(request):
    g_context = get_global_context(request)
    if 'maintenance' not in g_context['allowed_routes']:
        messages.error(request, "Access denied to Fleet Maintenance.")
        return redirect('dashboard')
        
    maintenance = request.session.get('maintenance', [])
    vehicles = request.session.get('vehicles', [])
    
    if request.method == 'POST' and 'action' in request.POST:
        action = request.POST.get('action')
        
        if action == 'create':
            new_id = max([m['id'] for m in maintenance]) + 1 if maintenance else 1
            new_log = {
                'id': new_id,
                'vehicle': request.POST.get('vehicle'),
                'type': request.POST.get('type'),
                'description': request.POST.get('description'),
                'cost': float(request.POST.get('cost') or 0),
                'date': request.POST.get('date', datetime.today().strftime('%Y-%m-%d')),
                'status': 'Open'
            }
            # Put vehicle in maintenance shop
            for v in vehicles:
                if v['registration_number'] in new_log['vehicle'] or v['name'] in new_log['vehicle']:
                    v['status'] = 'In Shop'
                    
            maintenance.append(new_log)
            request.session['maintenance'] = maintenance
            request.session['vehicles'] = vehicles
            messages.success(request, f"Maintenance Job #{new_id} created. Vehicle sent to Shop.")
            return redirect('maintenance')
            
        elif action == 'complete':
            log_id = int(request.POST.get('id'))
            for m in maintenance:
                if m['id'] == log_id:
                    m['status'] = 'Completed'
                    # Reset vehicle status to Available
                    for v in vehicles:
                        if v['registration_number'] in m['vehicle'] or v['name'] in m['vehicle']:
                            v['status'] = 'Available'
                    break
            request.session['maintenance'] = maintenance
            request.session['vehicles'] = vehicles
            messages.success(request, "Maintenance Job completed.")
            return redirect('maintenance')

    open_jobs = [m for m in maintenance if m['status'] == 'Open']
    completed_jobs = [m for m in maintenance if m['status'] == 'Completed']
    total_maint_cost = sum(m['cost'] for m in maintenance)
    
    context = {
        **g_context,
        'maintenance': maintenance,
        'open_jobs': open_jobs,
        'completed_jobs': completed_jobs,
        'total_maint_cost': total_maint_cost,
        'vehicles': vehicles
    }
    return render(request, 'maintenance.html', context)

# 6. FUEL & EXPENSES
@login_and_password_required
def expenses_view(request):
    g_context = get_global_context(request)
    if 'expenses' not in g_context['allowed_routes']:
        messages.error(request, "Access denied to Financial Operations.")
        return redirect('dashboard')
        
    fuel_logs = request.session.get('fuel_logs', [])
    expense_logs = request.session.get('expense_logs', [])
    maintenance = request.session.get('maintenance', [])
    vehicles = request.session.get('vehicles', [])
    
    if request.method == 'POST' and 'action' in request.POST:
        action = request.POST.get('action')
        
        if action == 'create':
            category = request.POST.get('category')
            amount = float(request.POST.get('amount') or 0)
            vehicle = request.POST.get('vehicle')
            date = request.POST.get('date', datetime.today().strftime('%Y-%m-%d'))
            description = request.POST.get('description')
            
            if category == 'Fuel':
                # Add to fuel logs
                new_fuel_id = max([f['id'] for f in fuel_logs]) + 1 if fuel_logs else 1
                fuel_logs.append({
                    'id': new_fuel_id,
                    'vehicle': vehicle,
                    'liters': round(amount / 1.85, 1),
                    'cost': amount,
                    'odometer': 0,
                    'date': date
                })
                request.session['fuel_logs'] = fuel_logs
            else:
                # Add to expense logs
                new_exp_id = max([e['id'] for e in expense_logs]) + 1 if expense_logs else 1
                expense_logs.append({
                    'id': new_exp_id,
                    'vehicle': vehicle,
                    'category': category,
                    'cost': amount,
                    'date': date,
                    'description': description
                })
                request.session['expense_logs'] = expense_logs
                
            messages.success(request, "Financial invoice recorded successfully!")
            return redirect('expenses')

    # Unify expense list for the template
    unified_expenses = []
    for f in fuel_logs:
        unified_expenses.append({
            'vehicle': f['vehicle'],
            'category': 'Fuel',
            'description': f"Refueled {f['liters']} Liters",
            'date': f['date'],
            'amount': f['cost']
        })
    for e in expense_logs:
        unified_expenses.append({
            'vehicle': e['vehicle'],
            'category': e['category'],
            'description': e['description'],
            'date': e['date'],
            'amount': e['cost']
        })
    for m in maintenance:
        unified_expenses.append({
            'vehicle': m['vehicle'],
            'category': 'Maintenance',
            'description': m['description'],
            'date': m['date'],
            'amount': m['cost']
        })
        
    # Sort descending by date
    unified_expenses = sorted(unified_expenses, key=lambda x: x['date'], reverse=True)
    
    # Calculate categories
    fuel_total = sum(f['cost'] for f in fuel_logs)
    maintenance_total = sum(m['cost'] for m in maintenance)
    other_total = sum(e['cost'] for e in expense_logs)
    total_cost = fuel_total + maintenance_total + other_total
    
    fuel_percent = (fuel_total / total_cost * 100) if total_cost > 0 else 0
    maintenance_percent = (maintenance_total / total_cost * 100) if total_cost > 0 else 0
    other_percent = (other_total / total_cost * 100) if total_cost > 0 else 0
    
    context = {
        **g_context,
        'expenses': unified_expenses,
        'total_cost': total_cost,
        'fuel_total': fuel_total,
        'maintenance_total': maintenance_total,
        'other_total': other_total,
        'fuel_percent': fuel_percent,
        'maintenance_percent': maintenance_percent,
        'other_percent': other_percent,
        'vehicles': vehicles
    }
    return render(request, 'expenses.html', context)

# 7. REPORTS & ANALYTICS
@login_and_password_required
def analytics_view(request):
    g_context = get_global_context(request)
    if 'analytics' not in g_context['allowed_routes']:
        messages.error(request, "Access denied to Reports & Analytics.")
        return redirect('dashboard')
        
    vehicles = request.session.get('vehicles', [])
    trips = request.session.get('trips', [])
    fuel_logs = request.session.get('fuel_logs', [])
    maintenance = request.session.get('maintenance', [])
    expense_logs = request.session.get('expense_logs', [])
    
    # Calculate costs
    total_maint = sum(m['cost'] for m in maintenance)
    total_fuel = sum(f['cost'] for f in fuel_logs)
    total_misc = sum(e['cost'] for e in expense_logs)
    total_cost = total_maint + total_fuel + total_misc
    
    # Fleet utilization percentage
    active_trips = sum(1 for t in trips if t['status'] == 'Dispatched')
    total_v = len(vehicles)
    fleet_utilization = int((active_trips / total_v) * 100) if total_v > 0 else 0
    
    # Avg trip cost
    avg_trip_cost = (total_cost / len(trips)) if trips else 0.0
    
    # Charts data mock
    charts = {
        'fleet_utilization_labels': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
        'fleet_utilization_data': [65, 78, 82, fleet_utilization],
        
        'vehicle_status_labels': ['Available', 'On Trip', 'In Shop', 'Retired'],
        'vehicle_status_data': [
            sum(1 for v in vehicles if v['status'] == 'Available'),
            sum(1 for v in vehicles if v['status'] == 'On Trip'),
            sum(1 for v in vehicles if v['status'] == 'In Shop'),
            sum(1 for v in vehicles if v['status'] == 'Retired')
        ]
    }
        
    context = {
        **g_context,
        'total_fuel': total_fuel,
        'total_maint': total_maint,
        'total_misc': total_misc,
        'total_trips': len(trips),
        'fleet_utilization': fleet_utilization,
        'avg_trip_cost': avg_trip_cost,
        'charts': charts,
        'charts_json': json.dumps(charts)
    }
    return render(request, 'analytics.html', context)

# 8. SETTINGS
@login_and_password_required
def settings_view(request):
    g_context = get_global_context(request)
    if 'settings' not in g_context['allowed_routes']:
        messages.error(request, "Access denied to Settings.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update_rbac':
            messages.success(request, "RBAC settings successfully saved.")
            return redirect('settings')
        elif action == 'notification_settings':
            messages.success(request, "Notification preferences updated.")
            return redirect('settings')
        elif action == 'app_preferences':
            messages.success(request, "Application global variables updated.")
            return redirect('settings')
        elif action == 'update_profile':
            name = request.POST.get('name')
            email = request.POST.get('email')
            avatar = request.POST.get('avatar')
            
            if name:
                request.session['user_name'] = name
            if email:
                request.session['user_email'] = email
            if avatar:
                request.session['user_avatar'] = avatar
                
            registered_users = request.session.get('registered_users', [])
            current_username = request.session.get('user_username')
            for u in registered_users:
                if u.get('username') == current_username:
                    if name: u['name'] = name
                    if email: u['email'] = email
                    break
            request.session['registered_users'] = registered_users
            
            messages.success(request, "Your profile details have been successfully updated.")
            return redirect('settings')
            
    # Mock Roles and detailed permissions for UI display
    role_matrix_table = [
        {'module': 'Dashboard', 'Admin': True, 'Fleet Manager': True, 'Driver': True, 'Safety Officer': True, 'Financial Analyst': True},
        {'module': 'Vehicles Registry', 'Admin': True, 'Fleet Manager': True, 'Driver': False, 'Safety Officer': False, 'Financial Analyst': False},
        {'module': 'Driver Profiles', 'Admin': True, 'Fleet Manager': False, 'Driver': False, 'Safety Officer': True, 'Financial Analyst': False},
        {'module': 'Trip Dispatcher', 'Admin': True, 'Fleet Manager': False, 'Driver': True, 'Safety Officer': False, 'Financial Analyst': False},
        {'module': 'Maintenance Logs', 'Admin': True, 'Fleet Manager': True, 'Driver': False, 'Safety Officer': False, 'Financial Analyst': False},
        {'module': 'Fuel & Operational Expenses', 'Admin': True, 'Fleet Manager': False, 'Driver': False, 'Safety Officer': False, 'Financial Analyst': True},
        {'module': 'Reports & Exports', 'Admin': True, 'Fleet Manager': True, 'Driver': False, 'Safety Officer': False, 'Financial Analyst': True},
        {'module': 'System Settings / RBAC', 'Admin': True, 'Fleet Manager': False, 'Driver': False, 'Safety Officer': True, 'Financial Analyst': False},
    ]
    
    context = {
        **g_context,
        'permissions': role_matrix_table,
        'user_email': request.session.get('user_email', ''),
        'user_username': request.session.get('user_username', ''),
    }
    return render(request, 'settings.html', context)

