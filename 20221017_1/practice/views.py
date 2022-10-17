from django.shortcuts import render, redirect
from .models import Practice

# Create your views here.

def index(request):
    return render(request, 'practice/index.html')

def new(request):
    return render(request, 'practice/new.html')

def create(request):
    title = request.GET.get('title')
    content = request.GET.get('content')
    Practice.objects.create(title=title, content=content)
    return redirect('practice:index')