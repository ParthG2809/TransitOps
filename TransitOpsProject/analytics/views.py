# analytics/views.py
from django.shortcuts import render
from common.decorators import login_and_password_required, role_required
from analytics.services import AnalyticsService

@login_and_password_required
@role_required(['Admin', 'Fleet Manager', 'Financial Analyst'])
def analytics_view(request):
    fleet_utilization = AnalyticsService.get_fleet_utilization()
    avg_trip_cost = AnalyticsService.get_avg_trip_cost()
    charts_json = AnalyticsService.get_charts_json()

    context = {
        'fleet_utilization': fleet_utilization,
        'avg_trip_cost': avg_trip_cost,
        'charts_json': charts_json
    }
    return render(request, 'analytics.html', context)
