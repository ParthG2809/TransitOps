# maintenance/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum
from common.decorators import login_and_password_required, role_required
from maintenance.models import Maintenance
from vehicles.models import Vehicle
import datetime
import re

@login_and_password_required
@role_required(['Admin', 'Fleet Manager', 'Financial Analyst'])
def maintenance_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'create':
            vehicle_raw = request.POST.get('vehicle', '').strip()
            m_type = request.POST.get('type', 'Routine').strip()
            cost = float(request.POST.get('cost') or 0.0)
            date_str = request.POST.get('date', '').strip()
            description = request.POST.get('description', '').strip()

            # Extract registration number from vehicle_raw (e.g. "Volvo Flatbed (MH-12-Q-9088)")
            reg_match = re.search(r'\(([^)]+)\)', vehicle_raw)
            reg_number = reg_match.group(1) if reg_match else vehicle_raw

            vehicle = Vehicle.objects.filter(registration_number=reg_number).first()

            if not vehicle:
                messages.error(request, f"Vehicle '{vehicle_raw}' not found.")
            else:
                try:
                    start_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else datetime.date.today()
                except ValueError:
                    start_date = datetime.date.today()

                m = Maintenance.objects.create(
                    vehicle=vehicle,
                    maintenance_type=m_type,
                    cost=cost,
                    start_date=start_date,
                    description=description,
                    technician="TransitOps Workshop Partner",
                    status='Open',
                    created_by=request.user if request.user.is_authenticated else None
                )

                # Update vehicle status to 'In Shop'
                vehicle.status = 'In Shop'
                vehicle.save()

                messages.success(request, f"Maintenance ticket opened for vehicle {vehicle.registration_number}.")

        elif action == 'complete':
            m_id = request.POST.get('id')
            m = Maintenance.objects.filter(id=m_id).first()
            if m:
                m.status = 'Completed'
                m.end_date = datetime.date.today()
                m.save()

                # Set vehicle back to Available
                v = m.vehicle
                if v:
                    v.status = 'Available'
                    v.save()

                messages.success(request, f"Maintenance ticket #{m_id} marked Completed. Vehicle released.")
            else:
                messages.error(request, "Maintenance ticket not found.")

        return redirect('maintenance')
    # Get list
    q = request.GET.get('q', '').strip()
    maintenance_all = Maintenance.objects.all().order_by('-start_date')
    if q:
        maintenance_all = maintenance_all.filter(
            vehicle__registration_number__icontains=q
        ) | maintenance_all.filter(
            description__icontains=q
        )

    # Filter open/completed
    open_jobs = maintenance_all.filter(status='Open')
    completed_jobs = maintenance_all.filter(status='Completed')

    # Total cost of completed jobs
    total_maint_cost = completed_jobs.aggregate(total=Sum('cost'))['total'] or 0.0

    # Vehicles dropdown (exclude retired)
    vehicles = Vehicle.objects.exclude(status='Retired')

    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(maintenance_all, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'maintenance': page_obj,
        'page_obj': page_obj,
        'open_jobs': open_jobs,
        'completed_jobs': completed_jobs,
        'total_maint_cost': total_maint_cost,
        'vehicles': vehicles,
        'q': q
    }
    return render(request, 'maintenance.html', context)
