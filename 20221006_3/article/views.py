from django.shortcuts import render
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

    return render(request, "article/index.html")
