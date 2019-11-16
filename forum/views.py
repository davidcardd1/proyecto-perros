from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Topic, Thread, Usuario, Post
from django.contrib.auth.models import User
from .forms import RegistrationForm, NewThreadForm, SignUpForm, NewPostForm
from django.views.generic import ListView, DetailView
from django.contrib.auth import login as auth_login
from django.db.models import Q


#forum
def home(request):
    return render(request, 'index.html')

def foro(request):
    queryset =request.GET.get("buscar") 
    #print(queryset)
    topics = Topic.objects.all()
    if queryset:
        topics = Topic.objects.filter(
            Q(name__icontains = queryset) |
            Q(description__icontains = queryset)
        ).distinct()
        
        return render(request, 'foro.html', {'topics': topics})

    else:
        return render(request, 'foro.html', {'topics': topics})
    
def topic_threads(request, n):
    topic = get_object_or_404(Topic, name=n)
    return render(request, 'threads.html', {'topic': topic})

def new_thread(request, n):
    topic = get_object_or_404(Topic, name=n)
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
            return redirect('topic_threads', n=topic.name)
    else:
        form = NewThreadForm() 
    return render(request, 'new_thread.html', {'topic': topic, 'form': form})

def new_post(request, nTo, nTh):
    thread = get_object_or_404(Thread, topic__name=nTo, name=nTh)
    user = Usuario.objects.first()  #cambiar por usuario logeado

    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.thread = thread
            post.user = user
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