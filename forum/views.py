from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm, AuthenticationForm
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import Topic, Thread, Usuario, Post
from .forms import RegistrationForm, EditProfileForm,ProfileForm, NewThreadForm
from django.views.generic import ListView, DetailView
from django.contrib.auth import login,authenticate

#forum
def home(request):
    return render(request, 'index.html')

def foro(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        register_form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('foro')

            register_form.save()
            username1 = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            user1 = authenticate(username=username1, password=password1)
            if user1 is not None:
                login(request, user1)
                return redirect('foro')

    form = AuthenticationForm()
    register_form = RegistrationForm()

    context = {
        'topics' : Topic.objects.all(),
        'form' : form,
        'register_form' : register_form
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
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('foro')
    else:
        form = RegistrationForm()
    
    args = {'form':form}
    return render(request, 'reg_form.html', args)

def login_view(request,*args, **kwargs):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('foro')
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "login.html",
                    context={"form":form})

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
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        password_form = PasswordChangeForm(data=request.POST, user=request.user)
        
        if form.is_valid() and profile_form.is_valid() and password_form.is_valid():
            password_form.save()
            user_form = form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            update_session_auth_hash(request, password_form.user)
            return redirect('/profile')
    else:
        form = EditProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        password_form = PasswordChangeForm(user=request.user)
        args = {}
        args['form'] = form
        args['profile_form'] = profile_form
        args['password_form'] = password_form
        return render(request, 'edit_profile.html', args)
    return render(request, 'profile.html', args)

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
