import datetime
from contextlib import closing


from django.db import connection
from methodism import dictfetchone, dictfetchall

from django.contrib.auth.decorators import login_required
from django.contrib.sites import requests
from django.core.paginator import Paginator
from django.conf import   settings
from django.shortcuts import render,redirect

from app.models import User
from app.models import Spam

def notifis():
    sql = " select id, name, familya, phone from app_user where new=true and not ut = 1 limit 3"
    cnt = "SELECT COUNT(*) as cnt from app_user WHERE new=TRUE and not ut = 1 limit 1 "

    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        result = dictfetchall(cursor)

    with closing(connection.cursor()) as cursor:
        cursor.execute(cnt)
        cnt_result = dictfetchone(cursor)
    return {
        "notifis": result,
        "cntNot": cnt_result
    }

def list_members(request,tpe=None,new=False):
    kwargs = {"ut":tpe} if tpe else {}
    if request.user.ut  not in  [1,2]:
        return redirect("login")
    if new:
        kwargs['new']=new

    pagination = User.objects.filter(**kwargs).order_by('-pk')
    paginator = Paginator(pagination, settings.PAGINATE_BY)
    page_number = request.GET.get("page", 1)
    paginated = paginator.get_page(page_number)


    uzunlik = len(pagination) // settings.PAGINATE_BY
    if len(pagination) % settings.PAGINATE_BY:
        uzunlik += 1
    length = [x for x in range(1,uzunlik+1)]



    types ={
        3 : "doctor",
        2 : "admin",
        4 : "member"
    }

    ctx = {
        "roots" : paginated,
        "root_type" : types.get(tpe,'New'),
        "page_len" : length,
        "current_page" : int(page_number),
        "uzunlik" : uzunlik


    }
    ctx.update(notifis())
    return render(request,'page/members.html',ctx)

@login_required(login_url='login')
def banned(request,user_id,tpe,status=False):
    if request.user.ut  not in  [1,2]:
        return redirect("login")
    try:
        user = User.objects.filter(id=user_id).first()
        user.is_active = status
        user.new = False
        user.save()
    except:
        pass
    return redirect('members',tpe=tpe)

@login_required(login_url='login')
def grader(request,pk,ut,dut):

    if request.user.ut  not in  [1,2]:
        return redirect("login")

    if request.user.ut == 1:
        try:
            kwargs = {"id" :pk}
            user = User.objects.filter(**kwargs).first()
            user.ut = ut
            user.new = False
            user.save()

        except:
            pass
    else:
        pass

    return redirect('members', tpe=dut)


# @login_required(login_url="login")
# def spammer(request,pk,dut):
#     spam_user = Spam.objects.filter(user_id=request.user.id,active=True ).first()
#     print(spam_user)
#     print(request.POST)
#     if request.user.ut != 1:
#         return redirect("home")
#     try:
#         user = User.objects.filter(id=pk).first()
#         Spam.objects.create(user=user)
#     except:
#         pass
#     return redirect("members",tpe=dut)



