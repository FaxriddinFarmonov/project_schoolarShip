from celery import shared_task
from .models import EmailLog
import time

@shared_task
def send_email_task(email_id):
    try:
        log = EmailLog.objects.get(id=email_id)

        # Simulyatsiya - email yuborish uchun vaqt ketadi
        time.sleep(5)

        # Email yuborildi deb taxmin qilamiz
        log.status = "sent"
        log.save()
        return f"Email sent to {log.email}"
    except Exception as e:
        log.status = "failed"
        log.save()
        return str(e)
