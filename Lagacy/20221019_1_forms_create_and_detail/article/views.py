from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleForm
# Create your views here.

def index(request):
    articles = Article.objects.order_by('-pk')
    context = {
        'articles': articles
    }

    return render(request, 'article/index.html', context)

# def new(request):
#     article_form = ArticleForm()
#     context = {
#         'article_form': article_form
#     }
#     return render(request, 'article/new.html', context=context)

def create(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():
            article_form.save() 
            return redirect('article:index')
    else:
        article_form = ArticleForm()
    context = {
    'article_form': article_form
    }
    return render(request, 'article/new.html', context=context)

def detail(request, pk):
    article = Article.objects.get(pk=pk)
    context = {
        'article': article
    }
    return render(request, 'article/detail.html', context)