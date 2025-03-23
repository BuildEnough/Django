from django.urls import path
from . import views

app_name = 'sign_up'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('new/', views.new, name='new'),
]