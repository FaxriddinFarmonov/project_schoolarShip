from django.conf import settings
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
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

        if not user.check_password(password):
            return render(request, "page/auth/login.html", {"error": "Parol yoki Phone xato"})

        if not user.is_active:
            return render(request, "page/auth/login.html", {"error": "Profile Ban Qilingan"})

        code = random.randint(100000, 999999)
        send_sms(998951808802,code)
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

        # return redirect("otp")

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
        # send_sms(998951808802,code)
        key = code_decoder(code)

        otp = OTP.objects.create(
            key=key,
            phone=data["phone"],
            step='regis',
            by=1,
            extra={
                'phone': data["phone"],
                'password': code_decoder(data['pass']),
                'fname': data["name"],

            }
        )
        otp.save()

        request.session["code"] = code
        request.session["email"] =data['email']
        request.session["phone"] = otp.phone
        request.session["otp_token"] = otp.key

        # return redirect("otp")
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