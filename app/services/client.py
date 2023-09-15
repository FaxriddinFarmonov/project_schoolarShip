from app.models import Service
from django.shortcuts import render,redirect
def client_index(request):
    service = Service.objects.all()
    ctx={
        "roots" : service
    }
    return render(request,'page/client/main.html',ctx)
