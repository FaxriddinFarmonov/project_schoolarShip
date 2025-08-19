from django.db import models


class CardRestriction(models.Model):
    card_number = models.CharField(max_length=32)  # ExtRid
    max_value = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)  # optional qildik
    currency = models.CharField(max_length=10, null=True, blank=True)  # optional qildik

    # Response ma'lumotlari
    result = models.CharField(max_length=50, null=True, blank=True)
    approval_code = models.CharField(max_length=20, null=True, blank=True)
    card_id = models.CharField(max_length=20, null=True, blank=True)  # CardVsdc Id
    restriction_guid = models.CharField(max_length=100, null=True, blank=True)

    status = models.CharField(max_length=20, default="limited")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.card_number} - {self.status}"
