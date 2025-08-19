from django.db import models

class TerminalInfo(models.Model):
    terminal_id = models.IntegerField(null=True, blank=True, unique=True)  # unik qilib qo‘ydim
    result = models.CharField(max_length=50, null=True, blank=True)
    terminal_inst_id = models.IntegerField(null=True, blank=True)
    terminal_class_guid = models.CharField(max_length=100, null=True, blank=True)
    terminal_class_title = models.CharField(max_length=100, null=True, blank=True)
    terminal_name = models.CharField(max_length=100, null=True, blank=True)
    terminal_status = models.CharField(max_length=50, null=True, blank=True)
    terminal_dflt_ccy = models.IntegerField(null=True, blank=True)
    terminal_accept_cash = models.BooleanField(default=False)
    terminal_address = models.TextField(null=True, blank=True)  # yangi qo‘shildi ✅

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.terminal_name} ({self.terminal_id})"
