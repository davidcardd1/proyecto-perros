from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import Topic, Thread, Usuario, Post
from .forms import RegistrationForm, EditProfileForm, NewThreadForm, SignUpForm
from django.views.generic import ListView, DetailView
from django.contrib.auth import login as auth_login


#forum
def home(request):
    return render(request, 'index.html')

def foro(request):
    context = {
        'topics' : Topic.objects.all()
    }
    return render(request, 'foro.html', context)
    
def topic_threads(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    return render(request, 'threads.html', {'topic': topic})

def new_thread(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    user = Usuario.objects.first()  #cambiar por usuario logeado

    if request.method == 'POST':
        form = NewThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.topic = topic
            thread.user = user
            thread.save()
            post = Post.objects.create(
                body=form.cleaned_data.get('body'),
                thread=thread,
                user=user
            )
            return redirect('topic_threads', pk=topic.pk)
    else:
        form = NewThreadForm() 
    return render(request, 'new_thread.html', {'topic': topic, 'form': form})

#account
def register(request):
    if request.method =='POST':
        print("Aqui estoy")
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            msg='You have successfully Registered'
            return render(request,'login.html',{'msg':msg})
    else:
        form = RegistrationForm()
    
    args = {'form':form}
    return render(request, 'reg_form.html', args)

def signup(request):
    if request.method =='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'login.html', {'form': form})

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
    return render(request, 'profile.html', args)
