# taxapp/models.py
from django.db import models
from django.contrib.auth.models import User

class TaxRecord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    annual_income = models.DecimalField(max_digits=12, decimal_places=2)
    calculated_tax = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Tax Record"