from django.contrib.auth.decorators import login_required
from django.contrib.sites import requests
from django.core.paginator import Paginator
from django.conf import   settings
from django.shortcuts import render,redirect

from app.models import User


def list_members(request,tpe=None):
    kwargs = {"ut":tpe} if tpe else {}


    pagination = User.objects.filter(**kwargs).order_by('-pk')
    paginator = Paginator(pagination, settings.PAGINATE_BY)
    page_number = request.GET.get("page", 1)
    paginated = paginator.get_page(page_number)

    types ={
        3 : "doctor",
        2 : "admin",
        4 : "member"
    }

    ctx = {
        "roots" : paginated,
        "root_type" : types.get(tpe,'all')
    }
    return render(request,'page/members.html',ctx)

@login_required(login_url='login')
def banned(request,user_id,tpe,status=False):
    if not request.user.ut == 1:
        return redirect('home')
    try:
        user = User.objects.filter(id=user_id).first()
        user.is_active = status
        user.save()
    except:
        pass
    return redirect('members',tpe=tpe)

@login_required(login_url='login')
def grader(request,pk,ut,dut):
    if not request.user.ut == 1:
        return redirect('home')
    try:
        kwargs = {"id" :pk}
        user = User.objects.filter(**kwargs).first()
        user.ut = ut
        user.save()

    except:
        pass

    return redirect('members', tpe=dut)
