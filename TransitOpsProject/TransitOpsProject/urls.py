# TransitOpsProject/urls.py
from django.contrib import admin
from django.urls import path

# Import views from modular apps
from accounts import views as accounts_views
from dashboard import views as dashboard_views
from vehicles import views as vehicles_views
from drivers import views as drivers_views
from trips import views as trips_views
from maintenance import views as maintenance_views
from expenses import views as expenses_views
from analytics import views as analytics_views
from settings_app import views as settings_views
from reports import views as reports_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Accounts & Authentication
    path('login/', accounts_views.login_view, name='login'),
    path('logout/', accounts_views.logout_view, name='logout'),
    path('register/', accounts_views.register_view, name='register'),
    path('forgot-password/', accounts_views.forgot_password_view, name='forgot_password'),
    path('otp-verify/', accounts_views.otp_verify_view, name='otp_verify'),
    path('change-password/', accounts_views.change_password_view, name='change_password'),
    path('users/', accounts_views.users_view, name='users'),
    
    # Dashboard & Portals
    path('', dashboard_views.dashboard_view, name='dashboard'),
    
    # Fleet Assets Registry
    path('vehicles/', vehicles_views.vehicles_view, name='vehicles'),
    
    # Drivers Dossier
    path('drivers/', drivers_views.drivers_view, name='drivers'),
    path('safety/', drivers_views.safety_view, name='safety'),
    
    # Trips & Dispatches
    path('trips/', trips_views.trips_view, name='trips'),
    
    # Maintenance Workshop
    path('maintenance/', maintenance_views.maintenance_view, name='maintenance'),
    
    # Expenses Ledger
    path('expenses/', expenses_views.expenses_view, name='expenses'),
    
    # Operational Intelligence & Analytics
    path('analytics/', analytics_views.analytics_view, name='analytics'),
    
    # Profile Settings
    path('settings/', settings_views.settings_view, name='settings'),
    path('switch-role/', settings_views.switch_role_view, name='switch_role'),
    path('toggle-theme/', settings_views.toggle_theme_view, name='toggle_theme'),
    
    # Reports & Exports
    path('reports/export/', reports_views.export_report_view, name='export_report'),
]
