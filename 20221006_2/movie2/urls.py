from django.urls import path
from . import views

app_name = "movie2"


urlpatterns = [
    path("", views.index, name="index"),
]
