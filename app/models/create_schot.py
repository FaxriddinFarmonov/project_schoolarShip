from django.db import models
from datetime import datetime
from datetime import date
from app.models.create_customer import SubjectUpdate

class LinkSchot(models.Model):
    customer = models.ForeignKey(SubjectUpdate, on_delete=models.CASCADE)
    TypeRid = models.CharField(max_length=32)
    ClientRid = models.CharField(max_length=32)
    Rid = models.CharField(max_length=32, blank=True)

    # Qo‘shimcha maydonlar
    BranchName = models.CharField(max_length=100, blank=True)
    BranchCode = models.CharField(max_length=32, blank=True)
    InstName = models.CharField(max_length=100, blank=True)
    ContractRid = models.CharField(max_length=32, blank=True)
    ClientId = models.CharField(max_length=32, blank=True)
    Currency = models.CharField(max_length=8, blank=True)
    Balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    CreditHold = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    DebitHold = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    PlanItemGuid = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
