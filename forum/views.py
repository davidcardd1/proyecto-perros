from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm, AuthenticationForm
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import Topic, Thread, Usuario, Post
from .forms import RegistrationForm, EditProfileForm,ProfileForm, NewThreadForm,  NewThreadForm, SignUpForm, NewPostForm
from django.contrib.auth.decorators import login_required
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
    queryset =request.GET.get("buscar") 
    #print(queryset)
    topics = Topic.objects.all()
    if queryset:
        topics = Topic.objects.filter(
            Q(name__icontains = queryset) |
            Q(description__icontains = queryset)
        ).distinct()
        
        return render(request, 'foro.html', {'topics': topics, 'form': form, 'register_form': register_form})

    else:
        return render(request, 'foro.html', {'topics': topics, 'form': form, 'register_form': register_form})
    
def topic_threads(request, n):

    topic = get_object_or_404(Topic, name=n)
    tema =get_object_or_404(Topic, name=n)
    pk = tema.pk
    print(tema.pk)
    print(tema.name)
    threads1 =  Thread.objects.filter(topic = pk)
    for Thread1 in threads1:
     print(Thread1.name)
    context = {
        'topic' : get_object_or_404(Topic, name=n),
        'threads' : Thread.objects.filter(topic = pk),
    }
    queryset =request.GET.get("buscar") 
    print(queryset)
    if queryset:
        threads1=Thread.objects.filter(
         Q(name__icontains = queryset) &
          Q(topic = pk)
         )
        context = {
        'topic' : get_object_or_404(Topic, name=n),
        'threads' : threads1,
        }
        return render(request, 'threads.html',context)
    else:
        
        return render(request, 'threads.html',context)

@login_required
def new_thread(request, n):
    topic = get_object_or_404(Topic, name=n)
    #user = Usuario.objects.first()  #cambiar por usuario logeado

    if request.method == 'POST':
        form = NewThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.topic = topic
            thread.user = request.user
            thread.save()
            post = Post.objects.create(
                body=form.cleaned_data.get('body'),
                thread=thread,
                user=user
            )
            return redirect('topic_threads', n=topic.name)
    else:
        form = NewThreadForm() 
    return render(request, 'new_thread.html', {'topic': topic, 'form': form})

@login_required
def new_post(request, nTo, nTh):
    thread = get_object_or_404(Thread, topic__name=nTo, name=nTh)
    #user = Usuario.objects.first()  #cambiar por usuario logeado

    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.thread = thread
            post.user = request.user
            post.save()
            return redirect('thread_posts', nTo=thread.topic.name, nTh=thread.name)
    else:
        form = NewPostForm() 
    return render(request, 'new_post.html', {'thread': thread, 'form': form})

def thread_posts(request, nTo, nTh):
    thread = get_object_or_404(Thread, topic__name=nTo, name=nTh)
    return render(request, 'posts.html', {'thread': thread})

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

        if form.is_valid() and profile_form.is_valid():
            user_form = form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            return redirect('/profile')
    else:
        form = EditProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        args = {}
        args['form'] = form
        args['profile_form'] = profile_form
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
