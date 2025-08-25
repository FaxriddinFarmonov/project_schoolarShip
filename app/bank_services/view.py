from django.shortcuts import render, redirect
from .models import EmailLog
from .tasks import send_email_task

def send_email_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        message = request.POST.get("message")

        log = EmailLog.objects.create(email=email, message=message)

        # Taskni fon rejimida Celery ga yuboramiz
        send_email_task.delay(log.id)

        return redirect("email_list")

    return render(request, "send_email.html")
