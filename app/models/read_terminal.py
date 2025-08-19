from django.db import models

class TerminalRead(models.Model):
    terminal_id = models.IntegerField(unique=True, db_index=True)
    terminal_name = models.CharField(max_length=100, db_index=True)

    class_guid = models.CharField(max_length=64, blank=True, default="")
    inst_name = models.CharField(max_length=64, blank=True, default="")
    status = models.CharField(max_length=8, blank=True, default="")
    title = models.CharField(max_length=255, blank=True, default="")
    notes = models.TextField(blank=True, null=True)

    create_time = models.DateTimeField(null=True, blank=True)
    create_day = models.DateTimeField(null=True, blank=True)
    activate_time = models.DateTimeField(null=True, blank=True)

    default_ccy = models.IntegerField(null=True, blank=True)
    default_language = models.CharField(max_length=16, blank=True, default="")

    # Address barcha atributlari bilan JSON ko‘rinishda
    address = models.JSONField(null=True, blank=True)

    # Branch atributlari
    branch_id = models.IntegerField(null=True, blank=True)
    branch_rid = models.CharField(max_length=64, blank=True, default="")
    branch_code = models.CharField(max_length=32, blank=True, default="")
    owner_rid = models.CharField(max_length=64, blank=True, default="")  # masalan PTPTP

    # Oxirgi aloqa ma’lumotlari
    last_rq_time = models.DateTimeField(null=True, blank=True)
    last_resp_time = models.DateTimeField(null=True, blank=True)
    last_online_rrn = models.CharField(max_length=64, blank=True, default="")
    mac_error_cnt = models.IntegerField(default=0)

    # POS parametrlar
    host_password = models.CharField(max_length=128, blank=True, default="")
    issuer_cards = models.BooleanField(default=False)
    term_enhanced_password = models.CharField(max_length=128, blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.terminal_name} ({self.terminal_id})"
