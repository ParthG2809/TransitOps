# common/permissions.py
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

def sync_user_role_groups(user):
    """
    Synchronizes the user's role with Django Auth Groups.
    Creates the Group if it does not exist, and adds the user.
    """
    if not user.role:
        return
        
    group, created = Group.objects.get_or_create(name=user.role)
    
    # Clear other role groups
    roles = ['Admin', 'Fleet Manager', 'Driver', 'Safety Officer', 'Financial Analyst']
    for r in roles:
        if r != user.role:
            other_group = Group.objects.filter(name=r).first()
            if other_group:
                user.groups.remove(other_group)
                
    user.groups.add(group)
