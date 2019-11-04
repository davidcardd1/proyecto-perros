
from django.contrib import admin
from django.urls import path, include
from Proyecto4Patas.views import index,login_redirect
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('',login_redirect),
    path('admin/', admin.site.urls),
    path('login/', include('Apps.Login.urls')),
    path('foro/',include('Apps.Post.urls') ),
    path('index/',index),
]
