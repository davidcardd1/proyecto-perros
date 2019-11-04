from django.urls import path
<<<<<<< HEAD
from Apps.Login.views import login
=======
from Apps.Login.views import register, profile
>>>>>>> base1
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    #path('',login),
    path('', LoginView.as_view(template_name='login.html'), name="login"),
<<<<<<< HEAD
    path('logout/', LogoutView.as_view(template_name='logout.html'), name="logout"),
]
=======
    path('', LogoutView.as_view(template_name='Login/logout.html'), name="logout"),
    path('register/', register, name="register"),
    path('profile/', profile, name="profile")
]
>>>>>>> base1
