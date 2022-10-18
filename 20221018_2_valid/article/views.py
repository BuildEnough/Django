from django.shortcuts import redirect, render
from .models import Article
from .forms import ArticleForm

# Create your views here.

def index(request):
    articles = Article.objects.order_by('-pk')
    context = {
        'articles': articles
    }
    

    return render(request, 'article/index.html', context)

def new(request):
    article_form = ArticleForm()

    context = {
        'article_form': article_form
    }

    return render(request, 'article/new.html', context=context)

def create(request):
    article_form = ArticleForm(request.POST)
    
    if article_form.is_valid():
        article_form.save()
        return redirect('article:index')
    else:
        print('유효하지 않음')

        context = {
        'article_form': article_form
        }
        
        return render(request, 'article/new.html', context=context)
    # title = request.POST.get('title')
    # content = request.POST.get('content')
    # Article.objects.create(title=title, content=content)