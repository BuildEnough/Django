from django.shortcuts import redirect, render
from .models import Post

# Create your views here.

def index(request):
    posts= Post.objects.order_by('-pk')

    context = {
        'posts': posts
    }
    
    return render(request, 'post/index.html', context)


def new(request):
    return render(request, 'post/new.html')


def create(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    Post.objects.create(title=title, content=content)

    return redirect('post:index')