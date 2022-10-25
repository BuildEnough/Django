from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('new/', views.new, name='new'),
    path('<int:article_pk>/delete', views.delete, name='delete'),
    path('<int:article_pk>/detail', views.detail, name='detail'),
    path('<int:article_pk>/update', views.update, name='update'),
]