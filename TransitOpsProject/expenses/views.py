# expenses/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum
from common.decorators import login_and_password_required, role_required
from expenses.models import Expense
from vehicles.models import Vehicle
import datetime
import re

@login_and_password_required
@role_required(['Admin', 'Financial Analyst', 'Fleet Manager'])
def expenses_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'create':
            vehicle_raw = request.POST.get('vehicle', '').strip()
            category = request.POST.get('category', 'Other').strip()
            amount = float(request.POST.get('amount') or 0.0)
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
                    expense_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else datetime.date.today()
                except ValueError:
                    expense_date = datetime.date.today()

                Expense.objects.create(
                    vehicle=vehicle,
                    expense_type=category,
                    amount=amount,
                    description=description,
                    expense_date=expense_date
                )
                messages.success(request, f"Expense of ₹{amount:.2f} logged successfully for {vehicle.registration_number}!")

        return redirect('expenses')

    # Get list
    q = request.GET.get('q', '').strip()
    expense_all = Expense.objects.all().order_by('-expense_date')
    if q:
        expense_all = expense_all.filter(
            vehicle__registration_number__icontains=q
        ) | expense_all.filter(
            description__icontains=q
        ) | expense_all.filter(
            expense_type__icontains=q
        )

    # Calculate Totals
    total_cost = expense_all.aggregate(total=Sum('amount'))['total'] or 0.0
    
    fuel_total = expense_all.filter(expense_type='Fuel').aggregate(total=Sum('amount'))['total'] or 0.0
    maintenance_total = expense_all.filter(expense_type='Maintenance').aggregate(total=Sum('amount'))['total'] or 0.0
    
    # Other totals include anything that is not Fuel/Maintenance (e.g. Tolls, Parts, Insurance, Other)
    other_total = expense_all.exclude(expense_type__in=['Fuel', 'Maintenance']).aggregate(total=Sum('amount'))['total'] or 0.0

    # Calculate percentages
    if total_cost > 0:
        fuel_percent = (float(fuel_total) / float(total_cost)) * 100.0
        maintenance_percent = (float(maintenance_total) / float(total_cost)) * 100.0
        other_percent = (float(other_total) / float(total_cost)) * 100.0
    else:
        fuel_percent = 0.0
        maintenance_percent = 0.0
        other_percent = 0.0

    # Vehicles dropdown (exclude retired)
    vehicles = Vehicle.objects.exclude(status='Retired')

    context = {
        'expenses': expense_all,
        'total_cost': total_cost,
        'fuel_total': fuel_total,
        'maintenance_total': maintenance_total,
        'other_total': other_total,
        'fuel_percent': fuel_percent,
        'maintenance_percent': maintenance_percent,
        'other_percent': other_percent,
        'vehicles': vehicles,
        'q': q
    }
    return render(request, 'expenses.html', context)
