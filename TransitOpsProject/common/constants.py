# common/constants.py

ROLE_CHOICES = [
    ('Admin', 'Admin'),
    ('Fleet Manager', 'Fleet Manager'),
    ('Driver', 'Driver'),
    ('Safety Officer', 'Safety Officer'),
    ('Financial Analyst', 'Financial Analyst'),
]

ROLE_PERMISSIONS = {
    'Admin': ['dashboard', 'fleet', 'drivers', 'trips', 'maintenance', 'expenses', 'analytics', 'settings', 'users'],
    'Fleet Manager': ['dashboard', 'fleet', 'maintenance', 'analytics'], # Wait, trips and reports are also under Fleet Manager. Let's make sure trips is in Fleet Manager's allowed routes if required, or keep the matrix from views.py.
    # In views.py: 'Fleet Manager': ['dashboard', 'fleet', 'maintenance', 'analytics']
    # Let's align with the template expectations:
    # Sidebar tabs:
    # 'dashboard' -> Dashboard
    # 'fleet' -> Vehicles
    # 'drivers' -> Drivers
    # 'trips' -> Trips
    # 'maintenance' -> Maintenance
    # 'expenses' -> Fuel & Expenses
    # 'analytics' -> Analytics
    # 'settings' -> Settings
    # 'users' -> Users directory
}

# Standardized allowed routes for each role matching the template sidebar checks:
ROLE_ALLOWED_ROUTES = {
    'Admin': ['dashboard', 'fleet', 'drivers', 'trips', 'maintenance', 'expenses', 'analytics', 'settings', 'users', 'safety'],
    'Fleet Manager': ['dashboard', 'fleet', 'drivers', 'trips', 'maintenance', 'analytics'], 
    'Driver': ['dashboard', 'trips'], 
    'Safety Officer': ['dashboard', 'settings', 'safety'], 
    'Financial Analyst': ['dashboard', 'maintenance', 'expenses', 'analytics']
}

VEHICLE_STATUS_CHOICES = [
    ('Available', 'Available'),
    ('On Trip', 'On Trip'),
    ('In Shop', 'In Shop'),
    ('Retired', 'Retired'),
]

DRIVER_STATUS_CHOICES = [
    ('Available', 'Available'),
    ('On Trip', 'On Trip'),
    ('Off Duty', 'Off Duty'),
    ('Suspended', 'Suspended'),
]

TRIP_STATUS_CHOICES = [
    ('Draft', 'Draft'),
    ('Dispatched', 'Dispatched'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
]

MAINTENANCE_STATUS_CHOICES = [
    ('Open', 'Open'),
    ('Completed', 'Completed'),
]

MAINTENANCE_TYPE_CHOICES = [
    ('Routine', 'Routine'),
    ('Repair', 'Repair'),
    ('Inspection', 'Inspection'),
    ('Other', 'Other'),
]

EXPENSE_TYPE_CHOICES = [
    ('Parts', 'Parts'),
    ('Toll', 'Toll'),
    ('Insurance', 'Insurance'),
    ('Fuel', 'Fuel'),
    ('Maintenance', 'Maintenance'),
    ('Other', 'Other'),
]

