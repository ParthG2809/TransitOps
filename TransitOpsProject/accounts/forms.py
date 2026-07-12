# accounts/forms.py
from django import forms
from accounts.models import User

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'role', 'department', 'phone_number']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'full_name', 'role', 'department', 'phone_number']
