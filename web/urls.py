from django.urls import path
from . import views
from django.conf.urls import handler404
from django.contrib.auth.views import LogoutView
app_name = 'web'

urlpatterns=[
    path('', views.homepage, name='homepage'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('faq/', views.faq_page, name='faq'),
    path('terms_and_conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('user_review/', views.user_review, name='user_review'),
    path('policity/', views.policity, name='policity'),
    path('user_settings/', views.user_settings, name='user_settings'),
    path('activate_account/<str:username>/', views.activate_account, name='activate_account'),
    path('logout/', views.logout_view, name='logout'),
]