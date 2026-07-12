# expenses/models.py
from django.db import models
from common.constants import EXPENSE_TYPE_CHOICES
from vehicles.models import Vehicle

class Expense(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='expenses')
    expense_type = models.CharField(max_length=30, choices=EXPENSE_TYPE_CHOICES, default='Other')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    expense_date = models.DateField()

    @property
    def category(self):
        return self.expense_type

    @property
    def date(self):
        return self.expense_date

    def __str__(self):
        return f"{self.vehicle} - {self.expense_type} (₹{self.amount})"
