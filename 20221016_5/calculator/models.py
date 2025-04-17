from django.db import models

# Create your models here.

class Calculator(models.Model):
    number = models.IntegerField()
    