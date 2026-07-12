# expenses/forms.py
from django import forms
from expenses.models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['vehicle', 'expense_type', 'amount', 'description', 'expense_date']
