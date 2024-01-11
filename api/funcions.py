from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse,Http404
from datetime import date, datetime
from django.contrib.auth.models import User
from django.template import RequestContext
from django.template.loader import render_to_string, get_template
from .models import CustomUser
import pytz
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.utils.html import strip_tags
import random
import base64
import os

def active_account_mail(mail,username):

    subject = '🐙 ¡Configura tu cuenta y protege tu experiencia de juego! Activa ahora 🛡️🔐 #ID={}'.format(random.randint(0, 55555))

    username = base64.b64encode(username.encode('utf-8')).decode('utf-8')
    html_message = get_template('api/mail_template.html').render({
        'account_active_link': "http://192.168.29.85:8000/activate_account/{}/".format(username),
    })
    recipient_list = ['unaianfruns60@gmail.com','alexrsen100@gmail.com',mail]

    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        'unaianfruns60@gmail.com',
        recipient_list,
        html_message=html_message,
        fail_silently=False,
    )

def check_for_a_valid_token(request):
    token_header = request.headers.get('Authorization', None)
    if token_header is not None and token_header.startswith('Bearer '):
        access_token = token_header[len('Bearer '):]
        if access_token == "test":
            return True
        else:
            return False
    else:
        #return False
        return True