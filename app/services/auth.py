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
    if request.POST:
        data = request.POST
        user = User.objects.filter(email=data["email"]).first()

        if not user:
            return render(request, "page/auth/login.html", {"error": "Parol yoki Email xato"})

        if not user.check_password(data["password"]):
            return render(request, "page/auth/login.html", {"error": "Parol yoki Email xato"})

        if not user.is_active:
            return render(request, "page/auth/login.html", {"error": "Profile Ban Qilingan"})

        code = random.randint(100000, 999999)
        # send_sms(998951808802,code)
        key = code_decoder(code)

        otp = OTP.objects.create(
            key=key,
            email=user.email,
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
        user = User.objects.filter(email=data['email']).first()

        if user:
            return render(request, "page/auth/regis.html", {"error": "Siz kiritgan email band"})

        if data["pass"] != data["pass_conf"]:
            return render(request, "page/auth/regis.html", {"error": "Parollar mos kelmadi"})

        # user=User.objects.create_user(email=data["email"],
        #                               password=data["pass"],
        #                               fname=data["name"],
        #                               lname=data["familya"]
        #                               )

        code = random.randint(100000, 999999)
        # send_sms(998951808802,code)
        key = code_decoder(code)

        otp = OTP.objects.create(
            key=key,
            email=data["email"],
            step='regis',
            by=1,
            extra={
                'email': data["email"],
                'password': data["pass"],
                'fname': data["name"],
                'lname': data["familya"]
            }
        )
        otp.save()

        request.session["code"] = code
        request.session["email"] = otp.email
        request.session["otp_token"] = otp.key

        return redirect("otp")
        authenticate(request)
        login(request, user)
        return redirect('home')

    return render(request, "page/auth/regis.html")

@login_required(login_url='sign-in')
def sign_out(request):
    logout(request)
    return redirect('sign-in')


def profile(request):
    return render(request,'page/auth/profile.html')