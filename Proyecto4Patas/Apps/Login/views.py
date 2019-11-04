from django.shortcuts import render, redirect
#from django.http import HttpResponse
#from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
#from Login.forms import RegistrationForm
# Create your views here.

def register(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            msg='You have successfully Registered'
            return render(request,'/login',{'msg':msg})
    else:
        form = UserCreationForm()
    
    args = {'form':form}
    return render(request, 'reg_form.html', args)