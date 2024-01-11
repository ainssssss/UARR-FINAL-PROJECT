from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse,Http404
from datetime import date, datetime
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.template import RequestContext
from django.template.loader import render_to_string, get_template
from .models import CustomUser
import pytz
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.utils.html import strip_tags
import random
from django.contrib.auth.hashers import make_password
from .funcions import active_account_mail,check_for_a_valid_token
import base64
import os
from django.contrib.auth.hashers import check_password

def error_404_view(request, exception):
    return render(request, 'api/404.html')

def check_usr_exist(request, username, password):
    if check_for_a_valid_token(request):
        user_exists = CustomUser.objects.filter(username=username).exists()

        if user_exists:
            user = CustomUser.objects.get(username=username)

            if check_password(password, user.password):
                status_text = "Successfully"
                error_text = "Account witch this username and password exist"
                print(user.date_last_ban)
                if user.is_ban_right_now == True:
                    status_text = "Error"
                    error_text = "Account its banned"
            else:
                status_text = "Error"
                error_text = "Account witch this username and password not exist"
        else:
            status_text = "Error"
            error_text = "Account witch this username and password not exist"

    else:
        status_text = "Failed"
        error_text = "You don't have a valid token"
    data = {
            'Status' : status_text,
            'Context' : error_text,
            "Date" : datetime.now(pytz.timezone('Europe/Madrid')),
        }

    return JsonResponse(data)


def ban_user(request, username, password):
    if check_for_a_valid_token(request):
        user_exists = CustomUser.objects.filter(username=username).exists()

        if user_exists:
            user = CustomUser.objects.get(username=username)
            if check_password(password, user.password):
                status_text = "Successfully"
                error_text = "Account banned Sucessfully"
                user.is_ban_right_now = True
                tiempo_actual = datetime.now(pytz.timezone('Europe/Madrid'))
                tiempo_modificado = tiempo_actual + timedelta(days=3)
                user.date_last_ban = tiempo_modificado
                user.save()

            else:
                status_text = "Error"
                error_text = "Account witch this username and password not exist"
        else:
            status_text = "Error"
            error_text = "Account witch this username and password not exist"

    else:
        status_text = "Failed"
        error_text = "You don't have a valid token"
    data = {
            'Status' : status_text,
            'Context' : error_text,
            "Date" : datetime.now(pytz.timezone('Europe/Madrid')),
        }

    return JsonResponse(data)

def create_user(request,username,password,mail):
    if check_for_a_valid_token(request):
        user_exists = CustomUser.objects.filter(username=username).exists()
        valid_passwd = False
        valid_mail = False
        status_text = "Failed"
        error_text = ""
        if user_exists: error_text = "This username is aldery in use"

        if not user_exists:

            if "@" in mail and "." in mail:
                valid_mail = True
            else:
                error_text = "Insert a valid mail"

            if len(password) >= 8:
                valid_passwd = True
            else:
                error_text = "Insert a valid password, at list 8 characters"

            if valid_mail == True and valid_passwd == True:
                try:
                    user = CustomUser.objects.create_user(username=username, email=mail, password=password,
                                                          is_active=True, is_staff=False, number_of_bans=5)
                    user.save()
                    status_text = "Successfully"

                    error_text = "User Created successfully"

                    active_account_mail(mail,username)
                except Exception as e:
                    print(e)
                    error_text = "Something go really bad in the serverside"
    else:
        status_text = "Failed"
        error_text = "You don't have a valid token"
    data = {
            'Status' : status_text,
            'Context' : error_text,
            "Date" : datetime.now(pytz.timezone('Europe/Madrid')),
        }
    return JsonResponse(data)

def active_mail(request, username):
    if check_for_a_valid_token(request):
        try:
          username =  base64.b64decode(username).decode('utf-8')
          user_exists = CustomUser.objects.get(username=username)
        except:
            user_exists = False

        if user_exists:
            if not user_exists.is_mail_verified:
                user_exists.is_mail_verified = True
                user_exists.save()
                status_text = "Successfully"
                error_text = "User Verified Successfully"
            else:
                status_text = "Failed"
                error_text = "User already have the account verified"
        else:
            status_text = "Failed"
            error_text = "Account with this data don't exist"
    else:
        status_text ="Failed"
        error_text = "You don't have a valid token"

    data = {
            'Status' : status_text,
            'Context' : error_text,
            "Date" : datetime.now(pytz.timezone('Europe/Madrid')),
        }
    return JsonResponse(data)

def changepass(request,username,password):
    if check_for_a_valid_token(request):
        try:
          username =  base64.b64decode(username).decode('utf-8')
          user_exists = CustomUser.objects.get(username=username)
        except:
            user_exists = False
        if user_exists:
            password = base64.b64decode(password).decode('utf-8')
            if user_exists.password != password:
                user_exists.password = password
                user_exists.save()
                status_text = "Successfully"
                error_text = "New Password Set Successfully"
            else:
                status_text = "Failed"
                error_text = "The password its the same"
        else:
            status_text = "Failed"
            error_text = "Account with this data don't exist"
    else:
        status_text ="Failed"
        error_text = "You don't have a valid token"

    data = {
            'Status' : status_text,
            'Context' : error_text,
            "Date" : datetime.now(pytz.timezone('Europe/Madrid')),
        }
    return JsonResponse(data)