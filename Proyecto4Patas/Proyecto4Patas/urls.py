
from django.contrib import admin
from django.urls import path, include
from Proyecto4Patas.views import index,login_redirect
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('',login_redirect),
    path('admin/', admin.site.urls),
    #path('login/', LoginView.as_view(template_name='login.html'), name="login"),
    #path('logout/', LogoutView.as_view(template_name='logout.html'), name="logout"),
    path('login/',include('Apps.Login.urls') ),
    #path('logout/',include('Apps.Login.urls') ),
    path('foro/',include('Apps.Post.urls') ),
    path('index/',index),

]