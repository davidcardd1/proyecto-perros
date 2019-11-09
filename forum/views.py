from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Topic
from django.contrib.auth.models import User
from .forms import RegistrationForm
from django.contrib.auth.models import User

def home(request):
    return render(request, 'index.html')

def foro(request):
    topics = Topic.objects.all()
    return render(request, 'foro.html', {'topics': topics})

def register(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            msg='You have successfully Registered'
            return render(request,'login.html',{'msg':msg})
    else:
        form = RegistrationForm()
    
    args = {'form':form}
    return render(request, 'reg_form.html', args)

def profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'profile.html', args)
