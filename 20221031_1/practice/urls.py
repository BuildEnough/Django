from django.urls import path 
from . import views

app_name = 'practice'

urlpatterns = [
    path('index/', views.index, name='practice'),
]