from django.db import models

class EmailLog(models.Model):
    email = models.EmailField()
    message = models.TextField()
    status = models.CharField(max_length=20, default="pending")  # pending, sent, failed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.status}"
