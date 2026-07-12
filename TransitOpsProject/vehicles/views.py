# vehicles/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from common.decorators import login_and_password_required, role_required
from vehicles.models import Vehicle
import datetime

@login_and_password_required
@role_required(['Admin', 'Fleet Manager', 'Safety Officer'])
def vehicles_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'create':
            reg_num = request.POST.get('registration_number', '').strip()
            name = request.POST.get('name', '').strip()
            model = request.POST.get('model', '').strip()
            v_type = request.POST.get('type', '').strip()
            
            capacity_raw = request.POST.get('capacity', '').strip()
            # Clean capacity (extract numbers)
            capacity_str = ''.join(c for c in capacity_raw if c.isdigit() or c == '.')
            capacity = float(capacity_str) if capacity_str else 0.0
            
            cost = float(request.POST.get('cost') or 0)
            odometer = int(request.POST.get('odometer') or 0)
            status = request.POST.get('status', 'Available')

            # Indian localized default fields
            purchase_date = datetime.date.today()
            insurance_expiry = datetime.date.today() + datetime.timedelta(days=365)
            region = "MH-HQ"
            fuel_type = "Diesel"

            if not reg_num or not name:
                messages.error(request, "Registration number and Vehicle name are required.")
            elif Vehicle.objects.filter(registration_number=reg_num).exists():
                messages.error(request, f"Vehicle with registration number {reg_num} already exists.")
            else:
                Vehicle.objects.create(
                    registration_number=reg_num,
                    vehicle_name=name,
                    vehicle_model=model,
                    vehicle_type=v_type,
                    maximum_load_capacity=capacity,
                    current_odometer=odometer,
                    acquisition_cost=cost,
                    purchase_date=purchase_date,
                    insurance_expiry=insurance_expiry,
                    region=region,
                    fuel_type=fuel_type,
                    status=status
                )
                messages.success(request, f"Vehicle {reg_num} registered successfully!")

        elif action == 'edit':
            v_id = request.POST.get('id')
            vehicle = Vehicle.objects.filter(id=v_id).first()
            if vehicle:
                reg_num = request.POST.get('registration_number', '').strip()
                name = request.POST.get('name', '').strip()
                model = request.POST.get('model', '').strip()
                v_type = request.POST.get('type', '').strip()
                
                capacity_raw = request.POST.get('capacity', '').strip()
                capacity_str = ''.join(c for c in capacity_raw if c.isdigit() or c == '.')
                capacity = float(capacity_str) if capacity_str else 0.0

                cost = float(request.POST.get('cost') or 0)
                odometer = int(request.POST.get('odometer') or 0)
                status = request.POST.get('status', 'Available')

                vehicle.registration_number = reg_num
                vehicle.vehicle_name = name
                vehicle.vehicle_model = model
                vehicle.vehicle_type = v_type
                vehicle.maximum_load_capacity = capacity
                vehicle.acquisition_cost = cost
                vehicle.current_odometer = odometer
                vehicle.status = status
                vehicle.save()
                messages.success(request, f"Vehicle {reg_num} updated successfully!")
            else:
                messages.error(request, "Vehicle not found.")

        elif action == 'delete':
            v_id = request.POST.get('id')
            vehicle = Vehicle.objects.filter(id=v_id).first()
            if vehicle:
                vehicle.status = 'Retired'
                vehicle.save()
                messages.success(request, f"Vehicle '{vehicle.registration_number}' retired successfully.")
            else:
                messages.error(request, "Vehicle not found.")

        return redirect('vehicles')

    # Get list
    q = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()
    view_mode = request.GET.get('view', 'table').strip()

    vehicles = Vehicle.objects.all()
    if q:
        vehicles = vehicles.filter(
            registration_number__icontains=q
        ) | vehicles.filter(
            vehicle_name__icontains=q
        ) | vehicles.filter(
            vehicle_model__icontains=q
        )
    
    if status_filter:
        vehicles = vehicles.filter(status=status_filter)

    # dropdown/filter statuses
    statuses = ['Available', 'On Trip', 'In Shop', 'Retired']

    context = {
        'vehicles': vehicles,
        'q': q,
        'status_filter': status_filter,
        'statuses': statuses,
        'view_mode': view_mode
    }
    return render(request, 'vehicles.html', context)
