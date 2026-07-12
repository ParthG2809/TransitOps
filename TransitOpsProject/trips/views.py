# trips/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from common.decorators import login_and_password_required, role_required
from trips.models import Trip
from trips.services import TripService
from vehicles.models import Vehicle
from drivers.models import Driver
from django.utils import timezone
import re
import random

@login_and_password_required
@role_required(['Admin', 'Fleet Manager', 'Driver'])
def trips_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'dispatch':
            # This is dispatching a new route dispatch
            source = request.POST.get('source', '').strip()
            destination = request.POST.get('destination', '').strip()
            vehicle_raw = request.POST.get('vehicle', '').strip()
            driver_raw = request.POST.get('driver', '').strip()
            cargo_weight = float(request.POST.get('cargo_weight') or 0)
            distance = float(request.POST.get('distance') or 0)

            # Extract registration number from vehicle_raw (e.g. "Volvo Flatbed (MH-12-Q-9088)")
            reg_match = re.search(r'\(([^)]+)\)', vehicle_raw)
            reg_number = reg_match.group(1) if reg_match else vehicle_raw
            
            vehicle = Vehicle.objects.filter(registration_number=reg_number).first()
            driver = Driver.objects.filter(name=driver_raw).first()

            # Enforce that driver role can only dispatch for themselves
            active_role = request.session.get('user_role', 'Driver')
            if active_role == 'Driver':
                driver_prof = Driver.objects.filter(user=request.user).first()
                if not driver_prof:
                    driver_prof = Driver.objects.filter(name=request.user.full_name).first()
                if not driver_prof or driver != driver_prof:
                    messages.error(request, "Access Denied: Drivers can only assign themselves to trips.")
                    return redirect('trips')

            if not vehicle:
                messages.error(request, f"Assigned vehicle '{vehicle_raw}' not found.")
            elif not driver:
                messages.error(request, f"Assigned driver '{driver_raw}' not found.")
            elif not source or not destination:
                messages.error(request, "Source and Destination are required.")
            else:
                # Generate unique trip number
                trip_num = f"TRIP-{random.randint(1000, 9999)}"
                while Trip.objects.filter(trip_number=trip_num).exists():
                    trip_num = f"TRIP-{random.randint(1000, 9999)}"

                # Calculate revenue (e.g., Rs. 25 per km)
                revenue = distance * 25.0

                try:
                    trip = Trip.objects.create(
                        trip_number=trip_num,
                        source=source,
                        destination=destination,
                        vehicle=vehicle,
                        driver=driver,
                        cargo_weight=cargo_weight,
                        planned_distance=distance,
                        trip_revenue=revenue,
                        status='Draft',
                        dispatch_time=timezone.now(),
                        created_by=request.user if request.user.is_authenticated else None
                    )
                    
                    # Call dispatch service to update vehicle/driver status
                    TripService.dispatch_trip(trip)
                    messages.success(request, f"Trip {trip_num} successfully dispatched and authorized!")
                except ValidationError as e:
                    messages.error(request, f"Dispatch Validation: {e.message if hasattr(e, 'message') else str(e)}")
                except Exception as e:
                    messages.error(request, f"System Error: {str(e)}")

        elif action == 'complete':
            t_id = request.POST.get('id')
            trip = Trip.objects.filter(id=t_id).first()
            if trip:
                try:
                    # Provide default values if completing from button click
                    actual_dist = trip.planned_distance
                    fuel_used = float(trip.planned_distance) / 4.0 # Estimate 4 km per liter
                    TripService.complete_trip(trip, float(actual_dist), float(fuel_used))
                    messages.success(request, f"Trip {trip.trip_number} completed. Vehicle returned to Available state.")
                except ValidationError as e:
                    messages.error(request, f"Completion Error: {e.message if hasattr(e, 'message') else str(e)}")
                except Exception as e:
                    messages.error(request, f"System Error: {str(e)}")
            else:
                messages.error(request, "Trip manifest record not found.")

        elif action == 'cancel':
            t_id = request.POST.get('id')
            trip = Trip.objects.filter(id=t_id).first()
            if trip:
                try:
                    TripService.cancel_trip(trip)
                    messages.success(request, f"Trip {trip.trip_number} cancelled. Vehicle and Driver released.")
                except ValidationError as e:
                    messages.error(request, f"Cancellation Error: {e.message if hasattr(e, 'message') else str(e)}")
            else:
                messages.error(request, "Trip manifest record not found.")

        return redirect('trips')

    # Get lists
    q = request.GET.get('q', '').strip()
    trips = Trip.objects.all().order_by('-dispatch_time')
    if q:
        trips = trips.filter(
            trip_number__icontains=q
        ) | trips.filter(
            source__icontains=q
        ) | trips.filter(
            destination__icontains=q
        )

    # Restrict to Driver's own trips if current active role is Driver
    # But allow sandbox managers to see all
    active_role = request.session.get('user_role', 'Driver')
    driver_prof = None
    if request.user.is_authenticated:
        driver_prof = Driver.objects.filter(user=request.user).first()
        if not driver_prof:
            driver_prof = Driver.objects.filter(name=request.user.full_name).first()

    if active_role == 'Driver':
        if driver_prof:
            trips = trips.filter(driver=driver_prof)
        else:
            trips = trips.none()

    # Prepopulate dropdown options for form
    available_vehicles = Vehicle.objects.filter(status='Available')
    if active_role == 'Driver':
        if driver_prof:
            available_drivers = Driver.objects.filter(id=driver_prof.id)
        else:
            available_drivers = Driver.objects.none()
    else:
        available_drivers = Driver.objects.filter(status='Available')

    context = {
        'trips': trips,
        'q': q,
        'available_vehicles': available_vehicles,
        'available_drivers': available_drivers
    }
    return render(request, 'trips.html', context)
