from django.urls import path
from Apps.Login.views import login

urlpatterns = [
    path('',login),

]
