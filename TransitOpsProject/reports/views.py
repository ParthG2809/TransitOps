# reports/views.py
from django.shortcuts import render
from django.http import HttpResponse
from common.decorators import login_and_password_required, role_required
from reports.services import ReportService

@login_and_password_required
@role_required(['Admin', 'Fleet Manager', 'Financial Analyst'])
def export_report_view(request):
    """
    Triggers CSV/Excel file export dynamically.
    """
    response = ReportService.generate_excel_or_csv_export()
    response['Content-Disposition'] = 'attachment; filename="TransitOps_Master_Report.csv"'
    return response
