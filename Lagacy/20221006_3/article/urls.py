from django.urls import path
from . import views

app_name = "article"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("delete/<int:article_pk>", views.delete, name="delete"),
    
    path("edit", views.edit, name = "edit"),
]
