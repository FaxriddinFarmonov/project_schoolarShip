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


def get_schot(request):
    try:
        objects = LinkSchot.objects.all().order_by('-id')
        paginator = Paginator(objects, 5)

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        ctx = {
            'roots': page_obj,
        }

        print("Umumiy ma'lumotlar soni:", objects.count())
        return render(request, 'page/link_schot.html', ctx)
    except Exception as e:
        print("Xatolik:", e)
        return render(request, 'page/link_schot.html', {"error": 404})
