from django.urls import path
from Apps.Login.views import login
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    #path('',login),
    path('', LoginView.as_view(template_name='login.html'), name="login"),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name="logout"),
]