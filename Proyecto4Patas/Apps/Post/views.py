from django.shortcuts import render
from django.http import HttpResponse

def foro(request):
   # return HttpResponse('foro')
    return render(request,'foro.html')
