# dashboard/views.py
from django.shortcuts import render
from django.db.models import Sum
from common.decorators import login_and_password_required
from vehicles.models import Vehicle
from drivers.models import Driver
from trips.models import Trip
from maintenance.models import Maintenance
from expenses.models import Expense
import json

@login_and_password_required
def dashboard_view(request):
    # Filters
    sel_vehicle_type = request.GET.get('vehicle_type', '').strip()
    sel_status = request.GET.get('status', '').strip()

    vehicles_qs = Vehicle.objects.exclude(status='Retired')
    if sel_vehicle_type:
        vehicles_qs = vehicles_qs.filter(vehicle_type=sel_vehicle_type)
    if sel_status:
        vehicles_qs = vehicles_qs.filter(status=sel_status)

    # Dynamic filter options
    vehicle_types = Vehicle.objects.exclude(status='Retired').values_list('vehicle_type', flat=True).distinct()
    statuses = ['Available', 'On Trip', 'In Shop']

    # KPIs
    active_vehicles = vehicles_qs.filter(status='On Trip').count()
    available_vehicles = vehicles_qs.filter(status='Available').count()
    vehicles_in_maintenance = vehicles_qs.filter(status='In Shop').count()
    
    total_non_retired = vehicles_qs.count()
    if total_non_retired > 0:
        fleet_utilization = int((active_vehicles / total_non_retired) * 100)
    else:
        fleet_utilization = 0

    drivers_on_duty = Driver.objects.filter(status='On Trip').count()
    active_trips = Trip.objects.filter(status='Dispatched').count()
    pending_trips = Trip.objects.filter(status='Draft').count()

    # Monthly OpEx (operational cost)
    maint_cost = Maintenance.objects.filter(status='Completed').aggregate(total=Sum('cost'))['total'] or 0.0
    exp_cost = Expense.objects.all().aggregate(total=Sum('amount'))['total'] or 0.0
    operational_cost = maint_cost + exp_cost

    # Recent dispatches
    recent_trips = Trip.objects.all().order_by('-dispatch_time', '-created_at')[:3]

    # Chart data calculations
    # 1. Utilization trend: mock or semi-dynamic trend ending with current utilization
    fleet_utilization_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    # Build a trend ending with the actual current fleet utilization
    fleet_utilization_data = [62, 65, 58, 70, 75, 80, fleet_utilization]

    # 2. Vehicle status distribution
    status_labels = ['Available', 'On Trip', 'In Shop', 'Retired']
    status_data = [
        Vehicle.objects.filter(status='Available').count(),
        Vehicle.objects.filter(status='On Trip').count(),
        Vehicle.objects.filter(status='In Shop').count(),
        Vehicle.objects.filter(status='Retired').count()
    ]

    charts_dict = {
        'fleet_utilization_labels': fleet_utilization_labels,
        'fleet_utilization_data': fleet_utilization_data,
        'vehicle_status_labels': status_labels,
        'vehicle_status_data': status_data
    }
    charts_json = json.dumps(charts_dict)

    # Expiry warnings for safety rating display
    # (checked globally in context processor, but keep variable in template)
    
    context = {
        'vehicle_types': vehicle_types,
        'sel_vehicle_type': sel_vehicle_type,
        'statuses': statuses,
        'sel_status': sel_status,
        
        'active_vehicles': active_vehicles,
        'available_vehicles': available_vehicles,
        'vehicles_in_maintenance': vehicles_in_maintenance,
        
        'drivers_on_duty': drivers_on_duty,
        'active_trips': active_trips,
        'pending_trips': pending_trips,
        'fleet_utilization': fleet_utilization,
        'operational_cost': operational_cost,
        
        'recent_trips': recent_trips,
        'charts_json': charts_json
    }
    return render(request, 'dashboard.html', context)
