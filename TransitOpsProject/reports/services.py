# reports/services.py
import csv
from io import StringIO
from django.http import HttpResponse
from vehicles.models import Vehicle
from drivers.models import Driver
from trips.models import Trip
from fuel.models import FuelLog
from expenses.models import Expense

class ReportService:
    @staticmethod
    def generate_excel_or_csv_export():
        """
        Aggregates all operations data and yields a CSV file stream.
        """
        output = StringIO()
        writer = csv.writer(output)

        writer.writerow(["TransitOps ERP - Smart Transport Operations Platform Master Report"])
        writer.writerow([])

        # Vehicles section
        writer.writerow(["1. VEHICLES REGISTRY"])
        writer.writerow(["Reg Number", "Name", "Model", "Type", "Capacity", "Odometer", "Status"])
        for v in Vehicle.objects.all():
            writer.writerow([v.registration_number, v.vehicle_name, v.vehicle_model, v.vehicle_type, v.maximum_load_capacity, v.current_odometer, v.status])
        writer.writerow([])

        # Drivers section
        writer.writerow(["2. DRIVERS DOSSIER"])
        writer.writerow(["Name", "License Number", "Category", "Expiry Date", "Phone", "Email", "Safety Score", "Status"])
        for d in Driver.objects.all():
            writer.writerow([d.name, d.license_number, d.license_category, d.license_expiry, d.phone, d.email, d.safety_score, d.status])
        writer.writerow([])

        # Trips section
        writer.writerow(["3. DISPATCHED TRIPS"])
        writer.writerow(["Trip Number", "Source", "Destination", "Vehicle", "Driver", "Cargo Weight", "Distance", "Revenue", "Status"])
        for t in Trip.objects.all():
            writer.writerow([t.trip_number, t.source, t.destination, t.vehicle.registration_number, t.driver.name, t.cargo_weight, t.planned_distance, t.trip_revenue, t.status])
        writer.writerow([])

        # Expenses section
        writer.writerow(["4. OPERATIONAL EXPENSES"])
        writer.writerow(["Vehicle", "Expense Type", "Amount", "Description", "Date"])
        for e in Expense.objects.all():
            writer.writerow([e.vehicle.registration_number, e.expense_type, e.amount, e.description, e.expense_date])

        return HttpResponse(output.getvalue(), content_type='text/csv')
