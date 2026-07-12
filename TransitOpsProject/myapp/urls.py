from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('otp-verify/', views.otp_verify_view, name='otp_verify'),
    path('switch-role/', views.switch_role_view, name='switch_role'),
    path('toggle-theme/', views.toggle_theme_view, name='toggle_theme'),
    
    path('', views.dashboard_view, name='dashboard'),
    path('vehicles/', views.vehicles_view, name='vehicles'),
    path('drivers/', views.drivers_view, name='drivers'),
    path('trips/', views.trips_view, name='trips'),
    path('maintenance/', views.maintenance_view, name='maintenance'),
    path('expenses/', views.expenses_view, name='expenses'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('settings/', views.settings_view, name='settings'),
    path('users/', views.users_view, name='users'),
    path('change-password/', views.change_password_view, name='change_password'),
]
