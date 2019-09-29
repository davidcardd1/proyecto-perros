
from django.contrib import admin
from django.urls import path, include
from Proyecto4Patas.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('Apps.Login.urls')),
    path('foro/',include('Apps.Post.urls') ),
    path('index/',index),

]
