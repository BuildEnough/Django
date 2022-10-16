from django.shortcuts import render
from .forms import Sign_upForm

# Create your views here.

def index(request):
    return render(request, 'sign_up/index.html')

def new(request):
    sign_up_form= Sign_upForm()
    context = {
        'sign_up_form': sign_up_form
    }
    return render(request, 'sign_up/new.html', context=context)