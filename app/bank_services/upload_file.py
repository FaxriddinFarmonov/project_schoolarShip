from decimal import Decimal
from django.shortcuts import render, redirect
from django.urls import reverse
from app.forms import LinkSchotForm
from app.models import SubjectUpdate
from app.models.create_schot import LinkSchot
import requests
import xml.etree.ElementTree as ET
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from app.models.create_customer import SubjectUpdate
from serpapi import GoogleSearch
from pprint import pprint
from app.models.doctor import Kafedra

# views.py
from django.shortcuts import render, redirect
from app.services.forms.upload_form import FileUploadForm
from app.models.upload_file import UploadedFile

def upload_file_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('get_file')  # success sahifaga o‘tadi
    else:
        form = FileUploadForm()
    return render(request, 'page/upload_file.html', {
        "form": form,

        "pos": "form"
    })
