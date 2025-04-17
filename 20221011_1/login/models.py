import email
from django.db import models
from django.forms import CharField, EmailField

# Create your models here.

class Login(models.Model):
    username = CharField(max_length=15)
    email = EmailField(max_length=20)