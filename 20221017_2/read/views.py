from django.shortcuts import redirect, render
from .models import Read

# Create your views here.

def index(request):
    # reads = Read.objects.all('-pk')
    reads = Read.objects.order_by('-pk')

    context = {
        'reads': reads
    }

    return render(request, 'read/index.html', context)

def new(request):
    return render(request, 'read/new.html')

def create(request):
    title = request.GET.get('title')
    content = request.GET.get('content')
    Read.objects.create(title=title, content=content)
    return redirect('read:index')

