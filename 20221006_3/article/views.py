from django.shortcuts import render, redirect
from .models import Article

# Create your views here.


def index(request):
    _articles = Article.objects.all()
    context = {
        "articles": _articles,
    }

    return render(request, "article/index.html", context)


def create(request):
    content = request.GET.get("content_")
    Article.objects.create(content=content)

    return redirect("article:index")


def delete(request, article_pk):
    article_ = Article.objects.get(pk=article_pk)
    article_.delete()

    return redirect("article:index")

def edit(request):
    return render(request, "article/edit.html")