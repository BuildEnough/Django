from django.shortcuts import render, redirect
from .models import Practice
# Create your views here.

def index(request):
    practices = Practice.objects.order_by('-pk')
    context = {
        'practices': practices
    }
    return render(request, 'practice/index.html', context)

def new(request):
    return render(request, 'practice/new.html')

def create(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    Practice.objects.create(title=title, content=content)
    return redirect('practice:index')