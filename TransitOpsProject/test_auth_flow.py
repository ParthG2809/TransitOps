import os
import django
from django.test import Client
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TransitOpsProject.settings')
django.setup()
settings.ALLOWED_HOSTS = ['*']

def test_flow():
    client = Client()
    
    print("1. Accessing dashboard unauthenticated (should redirect to login)...")
    res = client.get('/', follow=True)
    print("Redirect chain:", res.redirect_chain)
    assert 'login' in res.redirect_chain[-1][0], "Failed redirect to login"
    
    print("2. Attempting registration access (should redirect to login)...")
    res = client.get('/register/', follow=True)
    assert 'login' in res.redirect_chain[-1][0], "Failed registration block"
    print("   Success: Registration blocked and redirected to login.")
    
    print("3. Logging in as Admin (admin@transitops.com / admin123)...")
    res = client.post('/login/', {'username_or_email': 'admin@transitops.com', 'password': 'admin123'}, follow=True)
    assert res.status_code == 200
    assert client.session.get('user_role') == 'Admin'
    print("   Success: Logged in as Admin.")
    
    print("4. Accessing user directory as Admin...")
    res = client.get('/users/')
    assert res.status_code == 200
    print("   Success: Accessed user directory.")
    
    print("5. Creating new Driver user 'driver_new' with temp password 'tempdriver123'...")
    res = client.post('/users/', {
        'action': 'create',
        'name': 'New Driver',
        'username': 'driver_new',
        'email': 'newdriver@transitops.com',
        'phone': '+1 (555) 8888',
        'role': 'Driver',
        'department': 'Logistics',
        'password': 'tempdriver123',
        'confirm_password': 'tempdriver123',
        'is_active': 'True'
    }, follow=True)
    assert res.status_code == 200
    
    # Verify new user is in the database list
    users = client.session.get('registered_users')
    new_user = next((u for u in users if u['username'] == 'driver_new'), None)
    assert new_user is not None, "User driver_new was not created"
    assert new_user['needs_password_change'] is True, "needs_password_change should be True"
    print("   Success: New Driver user created with needs_password_change = True.")
    
    print("6. Logging out Admin...")
    client.post('/logout/', follow=True)
    assert 'user_role' not in client.session
    print("   Success: Logged out Admin.")
    
    print("7. Logging in as new driver (should force change_password redirect)...")
    res = client.post('/login/', {'username_or_email': 'newdriver@transitops.com', 'password': 'tempdriver123'}, follow=True)
    assert 'change-password' in res.redirect_chain[-1][0], "Failed change password redirect"
    assert client.session.get('force_password_change') is True
    print("   Success: Login successful but redirected to change-password.")
    
    print("8. Attempting to access dashboard with force_password_change active (should redirect to change_password)...")
    res = client.get('/', follow=True)
    assert 'change-password' in res.redirect_chain[-1][0], "Failed to block dashboard access"
    print("   Success: Dashboard access blocked.")
    
    print("9. Submitting new permanent password...")
    res = client.post('/change-password/', {
        'new_password': 'permanent123',
        'confirm_password': 'permanent123'
    }, follow=True)
    assert res.status_code == 200
    assert 'change-password' not in res.redirect_chain[-1][0]
    assert client.session.get('force_password_change') is not True
    print("   Success: Password changed, redirected to dashboard.")
    
    print("10. Attempting to access User Directory as Driver (should redirect to dashboard due to RBAC)...")
    res = client.get('/users/', follow=True)
    assert 'users' not in res.redirect_chain[-1][0], "Failed RBAC block"
    print("   Success: Driver RBAC restriction verified.")
    
    print("\nALL 10 SECURITY AND AUTH WORKFLOW TEST STEPS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    test_flow()
