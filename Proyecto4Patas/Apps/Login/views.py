from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def login(request):
    #return HttpResponse('login')
    return render(request,'login.html')