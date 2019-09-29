from django.urls import path, include
from Apps.Post.views import foro

urlpatterns = [
    path('',foro),

]
