from django.shortcuts import render, redirect
from .models import Articles
from .forms import ArticleForm
# Create your views here.

def index(request):
    articles = Articles.objects.order_by('-pk')
    context = {
        'articles': articles
    }

    return render(request, 'articles/index.html', context)

def create(request):
    article_form = ArticleForm()
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/create.html', context)

def new(request):
    if request.method == 'POST':
        article_form  = ArticleForm(request.POST)
        if article_form.is_valid():
            article_form.save()
            return redirect('articles:index')
    else:
        article_form = ArticleForm()
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/create.html', context)

def delete(request, article_pk):
    article = Articles.objects.get(pk=article_pk)
    article.delete()
    return redirect('articles:index')

def detail(request, article_pk):
    article = Articles.objects.get(pk = article_pk)
    context = {
        'article': article
    }
    return render(request, 'articles/detail.html', context)

def update(request, article_pk):
    article = Articles.objects.get(pk=article_pk)
    if request.method == 'POST':
        article_form  = ArticleForm(request.POST, instance=article)
        if article_form.is_valid():
            article_form.save()
            return redirect('articles:index')
    else:
        article_form = ArticleForm(instance=article)
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/update.html', context)