from .models import Topic
from .forms import RegistrationForm, EditProfileForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.db.models import Q


def home(request):
    return render(request, 'index.html')

def foro(request):
    queryset =request.GET.get("buscar") 
    topics = Topic.objects.all()
    if queryset:
        topics = Topic.objects.filter(
            Q(name__icontains = queryset) |
            Q(description__icontains = queryset)
        ).distinct()
        return render(request, 'foro.html', {'topics': topics})
    else:
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

def editProfile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/profile')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'edit_profile.html', args)

def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/profile')
        else:
            return redirect('/profile/changePassword')
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'change_password.html', args)