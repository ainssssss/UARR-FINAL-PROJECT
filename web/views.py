import django.contrib.auth
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from api.models import CustomUser
from .models import faq,reviews
import requests
from django.contrib.auth import logout
def homepage(request):
    if request.user.is_authenticated:
        context = {
            'user_page': "/user_settings",
        }
        return render(request, 'web/homepage.html',context)
    else:
        context = {
            'user_page': "/login",
        }
    return render(request, 'web/homepage.html',context)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
                user_exists = CustomUser.objects.get(username=username)
                if user_exists.is_mail_verified == False:
                    data = {
                        'status': "You need to verify your account frist",
                    }
                    return render(request, 'web/login.html', data)
                django.contrib.auth.login(request, user)
                return redirect('/')
        else:
            data = {
                    'status': "user or password incorrect",
             }
            return render(request, 'web/login.html',data)
    return render(request, 'web/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        mail = request.POST.get('mail', '')
        password = request.POST.get('password', '')
        re_password = request.POST.get('repeat-password', '')

        url_format = "http://127.0.0.1:8000/api/create_user/{}/{}/{}".format(username,password,mail)
        response = requests.get(url_format)
        jsondata = response.json()
        if jsondata['Status'] == "Successfully":
            return render(request, 'web/login.html')

        else:
            data = {
                    'status': "{}".format(jsondata['Context']),
             }
            return render(request, 'web/register.html',data)


    return render(request, 'web/register.html')

def faq_page(request):

    faqs_search = faq.objects.all()

    context = {
        "faqs": faqs_search,
    }
    return render(request, 'web/faq.html',context)

def terms_and_conditions(request):
    return render(request, 'web/terms_and_conditions.html')


def activate_account(request,username):
    request_backend_activate_account = requests.get("http://127.0.0.1:8000/api/active_mail/{}/".format(username)).json()
    return render(request, 'web/account_activate.html')

def user_review(request):
    if request.user.is_authenticated:
        user_info = ""
        more_user_info = ""
    else:
        user_info = "disabled"
        more_user_info = "placeholder='ONLY-FOR-MEMBERS'"
    reviews_search = reviews.objects.all()
    context = {

        "reviews" : reviews_search,
        "user_info" : user_info,
        "more_user_info":more_user_info,

    }

    if request.method == 'POST':
        username = request.user.username
        comment = request.POST.get('comment', '')
        nueva_review = reviews(username=username, review=comment)
        nueva_review.save()

        return render(request, 'web/user_reviews.html', context)

    return render(request, 'web/user_reviews.html',context)

def policity(request):
    return render(request, 'web/policity.html')

def user_settings(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            usuario = request.user
            usuario.first_name = request.POST.get('frist_name', '')
            usuario.last_name = request.POST.get('second_name', '')
            usuario.email = request.POST.get('gmail', '')
            usuario.save()
            return redirect('/')

        context = {
            'username' : request.user.username,
        }
        return render(request, 'web/user_settings.html',context)

    else:
            return redirect('/login')

def logout_view(request):
    logout(request)
    return redirect('/')
