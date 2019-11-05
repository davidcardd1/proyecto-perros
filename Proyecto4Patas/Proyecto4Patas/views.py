from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
# Create your views here.

def index(request):
    #return HttpResponse('index')
    return render(request,'index.html')

def login_redirect(request):
    return redirect('/account')