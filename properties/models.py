from django.db import models
from django.contrib.auth.models import AbstractUser


class Property(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    location = models.CharField(max_length=100)
    features = models.TextField()

    def __str__(self):
        return self.name

class Unit(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='units')
    type_choices = [
        ('1BHK', '1BHK'),
        ('2BHK', '2BHK'),
        ('3BHK', '3BHK'),
        ('4BHK', '4BHK'),
    ]
    type = models.CharField(max_length=10, choices=type_choices)
    rent_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.property.name} - {self.type}"
    
class Tenant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    document_proofs = models.CharField(max_length = 200)

    def __str__(self):
        return self.name

class TenantAgreement(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE) 
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    agreement_end_date = models.DateField()
    monthly_rent_date = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.tenant.name} - {self.unit}"


