from django.urls import path
from . import views

app_name = 'practice'

urlpatterns =[
    path('index/', views.index, name='index'),
    path('new/', views.new, name='new'),
    path('create/', views.create, name='create'),
]