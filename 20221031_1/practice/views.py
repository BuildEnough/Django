from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'practice/index.html')

def new(request):
    return render(request, 'practice/new.html')

def create(request):
    return 