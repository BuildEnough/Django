from django.shortcuts import render, redirect
from .models import Article

# Create your views here.

def index(request):
    articles = Article.objects.order_by('-pk')
    context = {
        'articles': articles
    }
    return render(request, 'articles/index.html', context)

def create(request):
    return render(request, 'articles/create.html')

def new(request):
    title = request.GET.get('title')
    content = request.GET.get('content')
    Article.objects.create(title=title, content=content)
    return redirect('articles:index')