from django.db import models
from datetime import datetime
from datetime import date

# models.py
from django.db import models

class UploadedFile(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')  # 'uploads/' papkaga yuklanadi
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



from django.db import models
class CashWithdrawal(models.Model):
    timestamp = models.DateTimeField()  # Sana va vaqt
    pan = models.CharField(max_length=30)  # Karta raqami
    amount = models.DecimalField(max_digits=20, decimal_places=2)  # Miqdor
    currency = models.CharField(max_length=10, default='UZS')  # Valyuta
    solution = models.CharField(max_length=20)  # Yechim (C:20)

    def __str__(self):
        return f"{self.timestamp} | {self.pan} | {self.amount} {self.currency}"
