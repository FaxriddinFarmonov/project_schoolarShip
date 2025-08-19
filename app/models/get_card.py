from django.db import models

class CardInfo(models.Model):
    card_ext_rid = models.CharField(max_length=50)  # foydalanuvchi kiritgan karta kod
    card_id = models.CharField(max_length=50)
    pan = models.CharField(max_length=20)
    result = models.CharField(max_length=50)
    approval_code = models.CharField(max_length=20)
    contract_rid = models.CharField(max_length=50)
    product_rid = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    create_time = models.DateTimeField()
    activate_day = models.DateTimeField()
    activate_username = models.CharField(max_length=50)
    exp_time = models.DateTimeField()
    max_val = models.DecimalField(max_digits=20, decimal_places=2)
    ccy = models.CharField(max_length=10)
    pvv = models.CharField(max_length=10)
    emboss_name = models.CharField(max_length=100)
    track_name = models.CharField(max_length=100)
    print_name = models.CharField(max_length=150)
    total_amt_up_lmt = models.DecimalField(max_digits=20, decimal_places=2)
    total_amt_lw_lmt = models.DecimalField(max_digits=20, decimal_places=2)
    total_cnt_up_lmt = models.IntegerField()
    total_cnt_lw_lmt = models.IntegerField()
    invalid_cap_tries_cnt = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pan} - {self.status}"
