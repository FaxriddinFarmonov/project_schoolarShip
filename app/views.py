from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from app.models import Service
from app.services.derector import notifis


# Create your views here.
@login_required(login_url='login')
def index(request):
    service = Service.objects.all()
    ctx = {
        "services": service
    }

    if request.user.ut == 1:
        ctx.update(notifis())

    return render(request, "page/index.html",ctx)

def index212(request):
    service = Service.objects.all()
    ctx = {
        "services": service
    }

    if request.user.ut == 1:
        ctx.update(notifis())

    # return render(request, "page/index.html",ctx)
