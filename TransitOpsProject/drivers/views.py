# drivers/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from common.decorators import login_and_password_required, role_required
from drivers.models import Driver
import datetime

@login_and_password_required
@role_required(['Admin', 'Fleet Manager'])
def drivers_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'create':
            name = request.POST.get('name', '').strip()
            phone = request.POST.get('phone', '').strip()
            lic_num = request.POST.get('license_number', '').strip()
            lic_cat = request.POST.get('license_category', '').strip()
            lic_exp = request.POST.get('license_expiry', '').strip()
            safety = int(request.POST.get('safety_score') or 95)
            status = request.POST.get('status', 'Available')
            email = request.POST.get('email', '').strip()
            temp_password = request.POST.get('temporary_password', '').strip()

            # Normalize active state
            if status == 'Active':
                status = 'Available'
            elif status == 'On Duty':
                status = 'On Trip'

            if not name or not lic_num or not email or not temp_password:
                messages.error(request, "Name, License Number, Email, and Temporary Password are required.")
            elif Driver.objects.filter(license_number=lic_num).exists():
                messages.error(request, f"Driver with DL number {lic_num} already exists.")
            else:
                from accounts.models import User
                from accounts.services import UserService
                
                # Check email existence in User model
                if User.objects.filter(email=email).exists():
                    messages.error(request, f"User with email '{email}' already exists.")
                else:
                    # Generate a unique username
                    base_username = email.split('@')[0].lower().replace('.', '').replace('_', '')
                    username = base_username
                    counter = 1
                    while User.objects.filter(username=username).exists():
                        username = f"{base_username}{counter}"
                        counter += 1
                    
                    try:
                        # Create User and send temporary credentials mail via SMTP
                        user = UserService.create_user(
                            username=username,
                            email=email,
                            role='Driver',
                            full_name=name,
                            temporary_password=temp_password,
                            department='Logistics',
                            phone_number=phone
                        )
                        
                        # Create Driver profile linked to User
                        Driver.objects.create(
                            user=user,
                            name=name,
                            phone=phone,
                            license_number=lic_num,
                            license_category=lic_cat,
                            license_expiry=lic_exp,
                            safety_score=safety,
                            status=status,
                            email=email
                        )
                        messages.success(request, f"Driver {name} registered successfully! A credentials email was dispatched to {email}.")
                    except Exception as e:
                        messages.error(request, f"Failed to register driver: {str(e)}")

        elif action == 'edit':
            d_id = request.POST.get('id')
            driver = Driver.objects.filter(id=d_id).first()
            if driver:
                status = request.POST.get('status', 'Available')
                if status == 'Active':
                    status = 'Available'
                elif status == 'On Duty':
                    status = 'On Trip'

                driver.name = request.POST.get('name', '').strip()
                driver.phone = request.POST.get('phone', '').strip()
                driver.license_number = request.POST.get('license_number', '').strip()
                driver.license_category = request.POST.get('license_category', '').strip()
                driver.license_expiry = request.POST.get('license_expiry', '').strip()
                driver.safety_score = int(request.POST.get('safety_score') or 95)
                driver.status = status
                driver.save()
                messages.success(request, f"Driver {driver.name} profile updated successfully!")
            else:
                messages.error(request, "Driver not found.")

        elif action == 'suspend':
            d_id = request.POST.get('id')
            driver = Driver.objects.filter(id=d_id).first()
            if driver:
                driver.status = 'Suspended'
                driver.save()
                messages.success(request, f"Driver '{driver.name}' suspended successfully.")
            else:
                messages.error(request, "Driver not found.")

        elif action == 'delete':
            d_id = request.POST.get('id')
            driver = Driver.objects.filter(id=d_id).first()
            if driver:
                name = driver.name
                driver.delete()
                messages.success(request, f"Driver '{name}' profile deleted successfully.")
            else:
                messages.error(request, "Driver not found.")

        return redirect('drivers')

    # Get list
    q = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()
    view_mode = request.GET.get('view', 'cards').strip()

    drivers = Driver.objects.all()
    if q:
        drivers = drivers.filter(
            name__icontains=q
        ) | drivers.filter(
            license_number__icontains=q
        )
    
    if status_filter:
        # handle mappings
        mapped_status = status_filter
        if status_filter == 'Active':
            mapped_status = 'Available'
        elif status_filter == 'On Duty':
            mapped_status = 'On Trip'
        drivers = drivers.filter(status=mapped_status)

    # Expiry warnings calculation: expiring within 30 days
    today = datetime.date.today()
    warning_threshold = today + datetime.timedelta(days=30)
    expiry_warnings = Driver.objects.filter(license_expiry__lte=warning_threshold).count()

    statuses = ['Active', 'On Duty', 'Suspended']

    context = {
        'drivers': drivers,
        'q': q,
        'status_filter': status_filter,
        'statuses': statuses,
        'view_mode': view_mode,
        'expiry_warnings': expiry_warnings
    }
    return render(request, 'drivers.html', context)


@login_and_password_required
@role_required(['Admin', 'Safety Officer'])
def safety_view(request):
    from django.db.models import Avg
    from accounts.models import User
    from accounts.services import UserService
    import datetime

    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Add new safety officer (Admin only)
        if action == 'create_officer':
            if request.user.role != 'Admin':
                messages.error(request, "Permission denied. Only Admins can add new safety officers.")
                return redirect('safety')
                
            name = request.POST.get('name', '').strip()
            username = request.POST.get('username', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()
            dept = request.POST.get('department', '').strip() or 'Safety & Compliance'
            pwd = request.POST.get('temporary_password', '').strip()
            confirm_pwd = request.POST.get('confirm_password', '').strip()

            if pwd != confirm_pwd:
                messages.error(request, "Passwords do not match.")
            elif User.objects.filter(username=username).exists():
                messages.error(request, f"Username '{username}' already exists.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, f"Email '{email}' already exists.")
            else:
                try:
                    UserService.create_user(
                        username=username,
                        email=email,
                        role='Safety Officer',
                        full_name=name,
                        temporary_password=pwd,
                        department=dept,
                        phone_number=phone
                    )
                    messages.success(request, f"Safety Officer '{name}' created successfully. Temporary credentials sent to {email}.")
                except Exception as e:
                    messages.error(request, f"Error creating safety officer: {str(e)}")

        elif action == 'update_score':
            d_id = request.POST.get('id')
            score = request.POST.get('safety_score')
            driver = Driver.objects.filter(id=d_id).first()
            if driver and score:
                try:
                    driver.safety_score = max(0, min(100, int(score)))
                    driver.save()
                    messages.success(request, f"Updated safety score for {driver.name} to {driver.safety_score}/100.")
                except ValueError:
                    messages.error(request, "Invalid safety score value.")
            else:
                messages.error(request, "Driver or score value not found.")

        elif action == 'send_warning':
            d_id = request.POST.get('id')
            driver = Driver.objects.filter(id=d_id).first()
            if driver:
                # Mock sending an email warning
                from django.core.mail import send_mail
                from django.conf import settings
                subject = "TransitOps ERP - CRITICAL: Driver License Expiry Warning"
                message = (
                    f"Hello {driver.name},\n\n"
                    f"Our records indicate that your Driving License (DL: {driver.license_number}) "
                    f"is expiring on {driver.license_expiry}. Please renew your credentials and "
                    f"submit updated documentation to the Safety Desk immediately to avoid suspensions.\n\n"
                    f"Regards,\n"
                    f"Safety & Compliance Team"
                )
                try:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL or 'safety@transitops.in',
                        [driver.email],
                        fail_silently=False
                    )
                    driver.warning_sent = True
                    driver.save()
                    messages.success(request, f"Sent DL renewal warning notification to {driver.name} ({driver.email}).")
                except Exception as e:
                    messages.error(request, f"Failed to send email warning: {str(e)}")
            else:
                messages.error(request, "Driver record not found.")

        return redirect('safety')

    # Get data
    drivers = Driver.objects.all()
    avg_score = drivers.aggregate(avg=Avg('safety_score'))['avg'] or 95.0
    avg_score = round(float(avg_score), 1)

    today = datetime.date.today()
    limit_date = today + datetime.timedelta(days=30)
    expiring_drivers = Driver.objects.filter(license_expiry__lte=limit_date)
    
    # Leaderboard
    top_performers = Driver.objects.filter(safety_score__gte=90).order_by('-safety_score')
    under_training = Driver.objects.filter(safety_score__lt=80).order_by('safety_score')

    # Safety officers list
    safety_officers = User.objects.filter(role='Safety Officer')

    context = {
        'avg_score': avg_score,
        'expiring_warnings': expiring_drivers.count(),
        'expiring_drivers': expiring_drivers,
        'top_performers': top_performers,
        'under_training': under_training,
        'drivers': drivers,
        'safety_officers': safety_officers
    }
    return render(request, 'safety.html', context)

