from django.shortcuts import redirect, render
from .models import Article
from .forms import LoginForm
# Create your views here.

def index(request):
    return render(request, 'login/index.html')

def new(request):
    return render(request, 'login/new.html')

def create(request):
    if request.method=='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login:index')
    else:
        form = LoginForm()
    context = {
        'form': form,
    }
    return render(request, 'login/create.html', context)