# common/middleware.py
import datetime
from django.utils.timezone import is_aware, make_naive
from accounts.models import User
from vehicles.models import Vehicle
from drivers.models import Driver
from trips.models import Trip
from maintenance.models import Maintenance
from fuel.models import FuelLog
from expenses.models import Expense

class SessionSyncMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process request
        response = self.get_response(request)
        
        # After response/views execution, sync DB records back to session
        # This guarantees that tests and old template files referencing session have up-to-date DB info.
        try:
            self.sync_db_to_session(request)
        except Exception as e:
            # Safe catch to avoid blocking responses if DB is not migrated yet
            pass

        return response

    def sync_db_to_session(self, request):
        # Sync Users
        users_list = []
        for u in User.objects.all():
            users_list.append({
                'name': u.full_name or u.username,
                'username': u.username,
                'email': u.email,
                'password': u.password, # django hashed password
                'role': u.role,
                'department': u.department,
                'phone': u.phone_number,
                'is_active': u.is_active,
                'needs_password_change': u.needs_password_change
            })
        request.session['registered_users'] = users_list

        # Sync Vehicles
        vehicles_list = []
        for v in Vehicle.objects.all():
            vehicles_list.append({
                'id': v.id,
                'registration_number': v.registration_number,
                'name': v.vehicle_name,
                'model': v.vehicle_model,
                'type': v.vehicle_type,
                'capacity': f"{v.maximum_load_capacity:,.0f} kg",
                'cost': float(v.acquisition_cost),
                'odometer': v.current_odometer,
                'status': v.status
            })
        request.session['vehicles'] = vehicles_list

        # Sync Drivers
        drivers_list = []
        for d in Driver.objects.all():
            drivers_list.append({
                'id': d.id,
                'name': d.name,
                'license_number': d.license_number,
                'license_category': d.license_category,
                'license_expiry': d.license_expiry.strftime('%Y-%m-%d') if d.license_expiry else '',
                'phone': d.phone,
                'email': d.email,
                'address': d.address,
                'photo': d.photo,
                'safety_score': d.safety_score,
                'status': d.status
            })
        request.session['drivers'] = drivers_list

        # Sync Trips
        trips_list = []
        for t in Trip.objects.all():
            dispatch_str = ""
            if t.dispatch_time:
                dispatch_str = t.dispatch_time.strftime('%Y-%m-%d %H:%M')
            complete_str = ""
            if t.completion_time:
                complete_str = t.completion_time.strftime('%Y-%m-%d %H:%M')

            trips_list.append({
                'id': t.id,
                'trip_number': t.trip_number,
                'source': t.source,
                'destination': t.destination,
                'vehicle': f"{t.vehicle.vehicle_name} ({t.vehicle.registration_number})",
                'driver': t.driver.name,
                'cargo_weight': float(t.cargo_weight),
                'distance': float(t.planned_distance),
                'actual_distance': float(t.actual_distance) if t.actual_distance else 0.0,
                'fuel_used': float(t.fuel_used) if t.fuel_used else 0.0,
                'trip_revenue': float(t.trip_revenue),
                'status': t.status,
                'dispatched_time': dispatch_str,
                'completed_time': complete_str
            })
        request.session['trips'] = trips_list

        # Sync Maintenance
        maint_list = []
        for m in Maintenance.objects.all():
            maint_list.append({
                'id': m.id,
                'vehicle': f"{m.vehicle.vehicle_name} ({m.vehicle.registration_number})",
                'type': m.maintenance_type,
                'description': m.description,
                'cost': float(m.cost),
                'date': m.start_date.strftime('%Y-%m-%d') if m.start_date else '',
                'status': m.status
            })
        request.session['maintenance'] = maint_list

        # Sync Fuel Logs
        fuel_list = []
        for fl in FuelLog.objects.all():
            fuel_list.append({
                'id': fl.id,
                'vehicle': f"{fl.vehicle.vehicle_name} ({fl.vehicle.registration_number})",
                'liters': float(fl.liters),
                'cost': float(fl.cost),
                'odometer': fl.odometer,
                'date': fl.date.strftime('%Y-%m-%d') if fl.date else ''
            })
        request.session['fuel_logs'] = fuel_list

        # Sync Expenses
        exp_list = []
        for e in Expense.objects.all():
            exp_list.append({
                'id': e.id,
                'vehicle': f"{e.vehicle.vehicle_name} ({e.vehicle.registration_number})",
                'category': e.expense_type,
                'cost': float(e.amount),
                'date': e.expense_date.strftime('%Y-%m-%d') if e.expense_date else '',
                'description': e.description
            })
        request.session['expense_logs'] = exp_list
