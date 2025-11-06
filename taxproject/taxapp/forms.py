# taxapp/forms.py
from django import forms

class IncomeForm(forms.Form):
    annual_income = forms.DecimalField(
        label="Your Total Annual Income (in ৳)",
        min_value=0,
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )