from django.db import models

from django.db import models


class CardModify(models.Model):
    # Foydalanuvchidan keladigan ma'lumotlar
    extrid = models.CharField("ExtRid", max_length=50)

    contract2rid = models.CharField("Contract2Rid", max_length=100)
    cur_branch_code = models.CharField("CurBranchCode", max_length=50)

    # Tashqi serverdan qaytadigan javob
    response_id = models.CharField(max_length=100, blank=True, null=True)
    result = models.CharField(max_length=50, blank=True, null=True)
    approval_code = models.CharField(max_length=50, blank=True, null=True)
    cardvsdc_id = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CardModify({self.extrid}) - {self.result or 'Pending'}"
