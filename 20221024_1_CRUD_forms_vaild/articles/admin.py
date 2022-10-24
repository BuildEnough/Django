from django.contrib import admin
from .models import Articles
# Register your models here.
# python3 manage.py createsuperuser: 아이디 만들기(터미널에 입력)
# 아이디: qwerty
# 비번: q1w2
admin.site.register(Articles)

