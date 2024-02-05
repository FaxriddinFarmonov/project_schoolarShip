from django.conf import settings
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
import datetime
import random
import datetime
from app.base.helper import send_sms
from django.shortcuts import render, redirect
from app.models.auth import User, OTP
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from methodism import code_decoder


def sign_in(request):
    if not request.user.is_anonymous:
        return redirect("home")
    ctx ={

    }
    if request.POST:
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        user = User.objects.filter(phone=phone).first()

        if not user:
            return render(request, "page/auth/login.html", {"error": "Parol yoki Phone xato"})

        if not user.is_active:
            ctx['error'] = 'Uzur siz blokdasiz sizga kirish mumkin emas'
            ctx['etype'] = 'ban'
            return render(request, "page/auth/login.html", ctx)


        if not user.check_password(password):
            return render(request, "page/auth/login.html", {"error": "Parol yoki Phone xato"})

        if not user.is_active:
            return render(request, "page/auth/login.html", {"error": "Profile Ban Qilingan"})

        code = random.randint(100000, 999999)

        # send_sms(phone,code)
        key = code_decoder(code)
        otp = OTP.objects.create(
            key=key,
            phone=user.phone,
            step='login',
            by=2
        )
        otp.save()
        request.session["id"] = user.id
        request.session["code"] = code
        request.session["email"] = user.email
        request.session["otp_token"] = otp.key

        return redirect("otp")

        login(request, user)
        return redirect("home")

    return render(request, "page/auth/login.html")


def sign_up(request):


    if request.POST:
        data = request.POST
        user = User.objects.filter(phone=data['phone']).first()
        print(user)

        if user:
            return render(request, "page/auth/regis.html", {"error": "Siz kiritgan phone band"})

        if data["pass"] != data["pass_conf"]:
            return render(request, "page/auth/regis.html", {"error": "Parollar mos kelmadi"})

        user=User.objects.create_user(phone=data["phone"],
                                      name=data['name'],
                                      email=data['email'],
                                      password=data["pass"],
                                      gender=int(data['gender']),
                                      )

        code = random.randint(100000, 999999)

        # send_sms(data['phone'],code)
        key = code_decoder(code)

        otp = OTP.objects.create(
            key=key,
            phone=data["phone"],
            step='regis',
            by=1,
            extra={
                'phone': data["phone"],
                'password':key,
                'fname': data["name"],

            }
        )
        otp.save()
        request.session["id"] = user.id
        request.session["code"] = code
        request.session["email"] =data['email']
        request.session["phone"] = otp.phone
        request.session["otp_token"] = otp.key

        return redirect("otp")
        authenticate(request)
        login(request, user)
        return redirect('home')

    return render(request, "page/auth/regis.html")


@login_required(login_url='login')
def sign_out(request):

    if request.user.is_anonymous:
        return redirect('home')
    logout(request)

    return redirect('login')

@login_required(login_url='login')
def profile(request):
    return render(request,'page/auth/profile.html')
@login_required(login_url='login')
def search(request,q):
    return render(request,'search.html')


def otp(request):
    if not request.session.get("otp_token"):
        return redirect("login")

    if request.POST:
        otp = OTP.objects.filter(key=request.session["otp_token"]).first()
        code = ''.join(x for x in request.POST.getlist('otp'))

        if not code.isdigit():
            return render(request, "page/auth/otp.html", {"error": "Harflar kiritmang!!!"})

        if otp.is_expire:
            otp.step = "faild"
            otp.save()
            return render(request, "page/auth/otp.html", {"error": "Token eskirgan!!!"})

        if (datetime.datetime.now() - otp.created).total_seconds() >= 120:
            otp.is_expire = True
            otp.save()
            return render(request, "page/auth/otp.html", {"error": "Vaqt tugadi!!!"})

        if int(code_decoder(otp.key, decode=True, l=1)) != int(code):
            otp.tries += 1
            otp.save()
            return render(request, "page/auth/otp.html", {"error": "Cod hato!!!"})

        if otp.by == 1:
            user = User.objects.get(id=request.session['id'])
            authenticate(request)
            otp.step = "registered"


        else:
            user = User.objects.get(id=request.session["id"])
            otp.step = "logged"

        login(request, user)
        otp.save()

        try:
            if 'user_id' in request.session:
                del request.session["id"]
                del request.session["code"]
                del request.session["email"]
                del request.session["otp_token"]
        except:
            pass

        return redirect("home")

    return render(request, "page/auth/otp.html")


def resent_otp(request):
    print('fafaf')
    if not request.session.get("otp_token"):
        return redirect("login")

    old = OTP.objects.filter(key=request.session["otp_token"]).first()
    old.step = 'failed'
    old.is_expire = True
    old.save()

    code = random.randint(100000, 999999)
    # send_sms(998951808802,code)
    key = code_decoder(code)

    otp = OTP.objects.create(
        key=key,
        phone=old.phone,
        step='login' if old.by == 2 else 'regis',
        by=old.by,
        extra=old.extra
    )
    otp.save()

    request.session["code"] = code
    request.session["phone"] = otp.phone
    request.session["otp_token"] = otp.key

    return redirect("otp")
