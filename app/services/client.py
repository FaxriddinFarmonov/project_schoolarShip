from app.models import Service
from django.shortcuts import render,redirect
def client_index(request,service=None   ):
    ctx = {

    }

    return render(request,'page/client/client_doc.html.html',ctx)
