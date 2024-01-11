from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404


urlpatterns = [
    path('',include('web.urls')),
    path('admin/', admin.site.urls),
    path('api/',include('api.urls')),
]
