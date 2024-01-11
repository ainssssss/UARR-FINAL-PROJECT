from django.urls import path
from . import views
from django.conf.urls import handler404
app_name = 'api'

urlpatterns=[
    path('create_user/<str:username>/<str:password>/<str:mail>/', views.create_user, name='create_user'),
    path('checkuser/<str:username>/<str:password>/', views.check_usr_exist, name='check_usr_exist'),
    path('changepass/<str:username>/<str:password>/', views.changepass, name='changepass'),
    path('ban_user/<str:username>/<str:password>/', views.ban_user, name='ban_user'),
    path('active_mail/<str:username>/', views.active_mail, name='active_mail'),
]