1. 가상환경 및 django 설치
   - `python -m venv [가상환경이름]`
   - `python -m venv venv`
   - 가상환경 폴더 `.gitignore` 설정


   <br>
   
   - 가상환경 실행한 후
   - `pip install django==[버전]`
   - `pip install django==3.2.13`
   - `pip list`
   - `pip freeze > requirements.txt`: pip 저장
   - `pip install -r requirements.txt`: pip 다운


<br>

---
2. 가상환경 실행 및 실행취소
   - `source [가상환경이름]/Scripts/activate`
   - `source venv/Scripts/activate`

   <br>

   - `. [가상환경이름]/Scripts/activate`
   - `. venv/Scripts/activate`
    
   <br>
   
   - Window: `source venv/Scripts/activate`
   - Mac: `source venv/bin/activate`

   <br>
   
   - `deactivate`

<br>

---

3. django 프로젝트 생성
   - `django-admin startproject [프로젝트_이름] [프로젝트_시작경로]`
   - `django-admin startproject pjt .`
   - `python manage.py runserver`: 서버 구동
   - 포트 변경: `python manage.py runserver [원하는 포트 번호]`
   - 포트 변경: `python manage.py runserver 8080`
   - 종료: `ctrl + c`

<br>

---

4. app 생성
   -`python manage.py startapp [생성할_app_이름]`
   - `python manage.py startapp articles`

<br>

---
5. app 등록
   - 프로젝트 파일의 `settings.py`
```python
# pjt/settings.py
INSTALLED_APPS = [
    'articles',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

<br>

---
6. url 설정
```python
# pjt/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls')),
]
```

```python
# articles/urls.py
from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('index/', views.index, name='index'),
]
```

<br>

---
7.  view. 설정
```python
# articles/urls.py
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'articles/index.html')
```

<br>

---
8. Template 생성
   - 전체 폴더 => 생성한 앱 => templates(폴더 생성) => articles(폴더 생성) => index.html(파일 생성)

<br>

---
9. templates 활용
   - 프로젝트 `settings.py` => `TEMPLATES`
   - `TEMPLATES` `DIRS`(경로) 지정
   ```python
   TEMPLATES = [
      {
         'BACKEND': 'django.template.backends.django.DjangoTemplates',
         'DIRS': [BASE_DIR / 'templates'],
         'APP_DIRS': True,
         'OPTIONS': {
               'context_processors': [
                  'django.template.context_processors.debug',
                  'django.template.context_processors.request',
                  'django.contrib.auth.context_processors.auth',
                  'django.contrib.messages.context_processors.messages',
               ],
         },
      },
   ]
   ```
   - 프로젝트와 동일한 경로 => `templates` 생성 (편한대로 바꿔도 됨)
   - 생성한 앱의 `views.py`에서 경로에 따라 `templates` => `base.html` 생성

<br>

---

10. base 설정
   - `base.html` => html `body`
   ```html
      {% block content %}
      {% endblock %}
   ```
   - `base.html`을 사용하는 html은 `{% extends 'base.html' %}` 사용
   ```html
      {% extends 'base.html' %}
      {% block content %}
      
      {% endblock %}
   ```

<br>

---
11. MODEL 정의
```python
# articles/models.py
class Article(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

<br>

---
12. Migrations 생성
   - `python manage.py makemigrations`

<br>

---
13. DB 반영(migrate)
   - `python manage.py migrate`
   - `python manage.py showmigrations` : migrate 확인
<br>

---

# CRUD 구현
14. CRUD-CREATE
   - url 생성
```python
# articles/urls.py
from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('create/', views.create, name='create'),
]
```
   - views 생성
```python
# articles/views.py
from django.shortcuts import render, redirect
from .models import Article

# Create your views here.
def index(request):
    return render(request, 'articles/index.html')

def create(request):
    return render(request, 'articles/create.html')

def new(request):
    title = request.GET.get('title')
    content = request.GET.get('content')
    Article.objects.create(title=title, content=content)
    return redirect('articles:index')
```
   - html 생성
```html
<!-- articles/templates/articles/create.html -->
{% extends 'base.html' %}
{% block content %}
<form action="{% url 'articles:new' %}">
    <label for="title">제목</label>
    <input type="text" name="title" id="title">
  
    <label for="content">내용:</label>
    <textarea name="content" id="" cols="30" rows="10"></textarea>
    <input type="submit" value="입력">
  </form>
{% endblock %}
```

<br>

---

15. CRUD-READ
   - views 수정
```python
# articles/views.py
def index(request):
    articles = Article.objects.order_by('-pk')
    context = {
        'articles': articles
    }
    return render(request, 'articles/index.html', context)
```
   - html 수정
```html
<!-- articles/templates/articles/index.html -->
{% extends 'base.html' %}
{% block content %}
<a href="{% url 'articles:create' %}">글 작성</a>

{% for article in articles %}
<h3>{{ article.title }}</h3>
<p>{{ article.content }}</p>
<p>{{ article.created_at }} {{ article.updated_at }}</p>
{% endfor %}
{% endblock %}
```

<br>

---

16. GET 방식 => POST 방식
   - views 수정
```python
# articles/views.py
from django.shortcuts import render, redirect
from .models import Article

# Create your views here.
def index(request):
    articles = Article.objects.order_by('-pk')
    context = {
        'articles': articles
    }
    return render(request, 'articles/index.html', context)

def create(request):
    return render(request, 'articles/create.html')

def new(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    Article.objects.create(title=title, content=content)
    return redirect('articles:index')
```
   - html 수정
```html
{% extends 'base.html' %}
{% block content %}
<form action="{% url 'articles:new' %}" method="POST">
    {% csrf_token %}
    <label for="title">제목</label>
    <input type="text" name="title" id="">
  
    <label for="content">내용:</label>
    <textarea name="content" id="" cols="30" rows="10"></textarea>
    <input type="submit" value="입력">
  </form>

<a href="{% url 'articles:index' %}">메인</a>
{% endblock %}
```

17. forms 방식
   - forms 생성
```python
# articles/forms.py
from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        # fields = '__all__'
        fields = ['title', 'content']
```
   - views 수정
```python
# articles/views.py
from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleForm

# Create your views here.
def index(request):
    articles = Article.objects.order_by('-pk')
    context = {
        'articles': articles
    }
    return render(request, 'articles/index.html', context)

def create(request):
    article_form = ArticleForm()
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/create.html', context)

def new(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    Article.objects.create(title=title, content=content)
    return redirect('articles:index')
```
   - html 수정
```html
<!-- articles/templates/articles/create.html -->
{% extends 'base.html' %}
{% block content %}
<form action="{% url 'articles:new' %}" method="POST">
    {% csrf_token %}
    {{ article_form.as_p }}
    <input type="submit" value="입력">
  </form>

<a href="{% url 'articles:index' %}">메인</a>
{% endblock %}
```

<br>

---
18. vaild 유효성 검사
   - views 수정
```python
def new(request):
    article_form = ArticleForm(request.POST)
    if article_form.is_valid():
        article_form.save()
        return redirect('articles:index')
    else:
        context = {
            'article_form': article_form
        }
        return render(request, 'articles/create.html', context)
```
   
<br>

---
19. detail 페이지 생성
   - urls 수정
```python
# articles/urls.py
from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('new/', views.new, name='new'),
    path('<int:pk>/detail', views.detail, name='detail'),
    
]
```
   - view.py
```python
# articles/views.py
from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleForm

# Create your views here.
def index(request):
    articles = Article.objects.order_by('-pk')
    context = {
        'articles': articles
    }
    return render(request, 'articles/index.html', context)

def new(request):
    article_form = ArticleForm(request.POST)
    if article_form.is_valid():
        article_form.save()
        return redirect('articles:index')
    else:
        article_form = ArticleForm()
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/create.html', context)

def detail(request, article_pk):
    article = Article.objects.get(article_pk)
    context = {
        'article': article
    }
    return render(request, 'articles/detail.html', context)
```
   - index html 수정
```html
<!-- articles/templates/articles/index.html -->
{% extends 'base.html' %}
{% block content %}
<a href="{% url 'articles:new' %}">글 작성</a>

{% for article in articles %}
<h3><a href="{% url 'articles:detail' article.pk %}">{{ article.title }}</a></h3>
<p>{{ article.content }}</p>
<p>{{ article.created_at }} {{ article.updated_at }}</p>
{% endfor %}
{% endblock %}
```
   - detail html 생성
```html
<!-- articles/templates/articles/detail.html -->
{% extends 'base.html' %}
{% block content %}
<h1>{{ article.pk }}번</h1>
<h2>{{ article.created_at }} | {{ article.updated_at }}</h2>
<p>{{ article.content }}</p>
{% endblock %}
```

<br>

---
20. CRUD-UPDATE
   - url 수정
```python
# articles/urls.py
from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('new/', views.new, name='new'),
    path('<int:article_pk>/detail', views.detail, name='detail'),
    path('<int:pk>/update', views.update, name='update'),
]
```
   - views 수정
```python
# articles/views.py
from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleForm

# Create your views here.
def index(request):
    articles = Article.objects.order_by('-pk')
    context = {
        'articles': articles
    }
    return render(request, 'articles/index.html', context)

def new(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():
            article_form.save()
            return redirect('articles:index')
    else:
        article_form = ArticleForm()
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/create.html', context)

def detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    context = {
        'article': article
    }
    return render(request, 'articles/detail.html', context)

def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, instance=article)
        if article_form.is_valid():
            article_form.save()
            return redirect('articles:detail', article.pk)
    else:
        article_form = ArticleForm(instance=article)
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/update.html', context)
```
   - html 수정
```html
<!-- articles/templates/articles/detail.html -->
{% extends 'base.html' %}
{% block content %}
<h1>{{ article.pk }}번</h1>
<h2>{{ article.created_at }} | {{ article.updated_at }}</h2>
<p>{{ article.content }}</p>

<a href="{% url 'articles:update' article.pk %}">글 수정</a>
{% endblock %}
```
   - html 생성
```html
<!-- articles/templates/articles/update.html -->
{% extends 'base.html' %}
{% block content %}
<h1>글 수정</h1>
<form action="" method="POST">
    {% csrf_token %}
    {{ article_form.as_p }}
    <input type="submit" value="수정">
</form>
{% endblock %}
```

<br>

---
21. CRUD-DELETE
   - views 수정
```python
# articles/urls.py
# delete path 추가
from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('new/', views.new, name='new'),
    path('<int:article_pk>/detail', views.detail, name='detail'),
    path('<int:pk>/update', views.update, name='update'),
    path('<int:pk>/delete', views.delete, name='delete'),
]
```
```python
# articles/views.py
# delete 함수 추가
def delete(request, pk):
    article = Article.objects.get(pk=pk)
    article.delete()
    return redirect('articles:index')
```
   - html 수정
```html
<!-- articles/templates/articles/index.html -->
{% extends 'base.html' %}
{% block content %}
<a href="{% url 'articles:new' %}">글 작성</a>

{% for article in articles %}
<h3><a href="{% url 'articles:detail' article.pk %}">{{ article.title }}</a></h3>
<p>{{ article.content }}</p>
<p>{{ article.created_at }} {{ article.updated_at }}</p>
<a href="{% url 'articles:delete' article.pk %}">글 삭제</a>
{% endfor %}
{% endblock %}
```
```html
<!-- articles/templates/articles/detail.html -->
{% extends 'base.html' %}
{% block content %}
<h1>{{ article.pk }}번</h1>
<h2>{{ article.created_at }} | {{ article.updated_at }}</h2>
<p>{{ article.content }}</p>

<a href="{% url 'articles:update' article.pk %}">글 수정</a>
<a href="{% url 'articles:index' %}">메인</a>
{% endblock %}
```  

<br>

---
22. admin
    - `$ python manage.py createsuperuser `
```python
# articles/admin.py
from django.contrib import admin
from .models import Article

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
admin.site.register(Article, ArticleAdmin)
```

<br>

---
23. static
- 폴더들을 모듈로 관리
- 생성한 앱 안에 `static` 폴더 생성 => `static` 폴더 안에 이미지(`cowboy.png`) 생성
- css도 같은 방법으로 사용할 수 있음

<br>

- `{% load static %}`, `img`태그 불러오기
  - html 수정
```html
<!-- articles/templates/articles/index.html -->
{% extends 'base.html' %}
{% block content %}
{% load static %}
<img src="{% static 'cowboy.png' %}" alt="">
<a href="{% url 'articles:new' %}">글 작성</a>

{% for article in articles %}
<h3><a href="{% url 'articles:detail' article.pk %}">{{ article.title }}</a></h3>
<p>{{ article.content }}</p>
<p>{{ article.created_at }} {{ article.updated_at }}</p>
<a href="{% url 'articles:delete' article.pk %}">글 삭제</a>
{% endfor %}
{% endblock %}
```

- 생성한 프로젝트의 `settings.py`안의 `STATIC_UR`에서 관리함
- `settings.py`
```python
# pjt/settings.py
STATIC_URL = '/static/'
```

<br>

- 생성한 앱 안에 `static` 폴더 생성 => `static` 폴더 안에 `images` 폴더 안에 이미지(`cowboy.png`) 생성
  - html 수정
```html
<!-- articles/templates/articles/index.html -->
{% extends 'base.html' %}
{% block content %}
{% load static %}
<img src="{% static 'images/cowboy.png' %}" alt="">
<a href="{% url 'articles:new' %}">글 작성</a>

{% for article in articles %}
<h3><a href="{% url 'articles:detail' article.pk %}">{{ article.title }}</a></h3>
<p>{{ article.content }}</p>
<p>{{ article.created_at }} {{ article.updated_at }}</p>
<a href="{% url 'articles:delete' article.pk %}">글 삭제</a>
{% endfor %}
{% endblock %}
```

<br>

---
24. bootstrap
- 터미널: `pip install django-bootstrap5`
```python
INSTALLED_APPS = (
# pjt/settings.py
    # ...
    "django_bootstrap5",
    # ...
)
```

<br>

- html 수정
```html
<!-- templates/base.html -->
{% load django_bootstrap5 %}
{% bootstrap_css %}
{% bootstrap_javascript %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <!-- <link rel="stylesheet" href="{/% static css/style.css /%}"> -->
</head>
<body>
    {% block content %}
    {% endblock %}
</body>
</html>
```

```html
<!-- articles/templates/articles/create.html -->
{% extends 'base.html' %}
{% load django_bootstrap5 %}
{% bootstrap_css %}
{% bootstrap_javascript %}
{% block content %}

<form action="" method="POST">
    {% csrf_token %}

    {# article_form.as_p #}
    {% comment %} <input type="submit" value="입력"> {% endcomment %}

    {% bootstrap_form article_form %}
    {% bootstrap_button button_type='submit' content='OK' %}
  </form>

<a href="{% url 'articles:index' %}">메인</a>
{% endblock %}
```

<br>

---
25. form 커스텀
```html
<!-- articles/templates/articles/create.html -->
{% extends 'base.html' %}
{% load django_bootstrap5 %}
{% bootstrap_css %}
{% bootstrap_javascript %}
{% block content %}

<form action="" method="POST">
    {% csrf_token %}

    {% for field in article_form %}
    <p>
      {{ field }}
    </p>
      {{ field.label_tag }}
    {% endfor %}

    {% bootstrap_form article_form %}
    {% bootstrap_button button_type='submit' content='OK' %}
  </form>

<a href="{% url 'articles:index' %}">메인</a>
{% endblock %}
```

<br>

- input 태그 자체 커스텀 위 html에선 `{{ field }}` 설정
  - forms.py 위젯 설정(autofocus, placeholder)
  - articles/forms.py widgets 설정

<br>

---
26. create, update 같은 페이지 사용
- `update.html` 파일 이름 => `form.html`로 변경
- `create 함수`, `update 함수`의  `return 값` 수정
```python
# article/views.py
def new(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():
            article_form.save()
            return redirect('articles:index')
    else:
        article_form = ArticleForm()
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/form.html', context)

def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, instance=article)
        if article_form.is_valid():
            article_form.save()
            return redirect('articles:detail', article.pk)
    else:
        article_form = ArticleForm(instance=article)
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/form.html', context)
```

<br>

---
27. 페이지 분기
- `request`
```html
<!-- articles/templates/articles/forms.html -->
{% extends 'base.html' %}
{% load django_bootstrap5 %}
{% bootstrap_css %}
{% bootstrap_javascript %}
{% block content %}
<h1>글 수정</h1>

{{ request.path }}
{{ request.GET }}

<form action="" method="POST">
    {% csrf_token %}
    {% bootstrap_form article_form %}
    {% bootstrap_button button_type='submit' content='OK' %}
    <input type="submit" value="수정">
</form>
{% endblock %}
```

```html
<!-- articles/templates/articles/forms.html -->
{% extends 'base.html' %}
{% load django_bootstrap5 %}
{% bootstrap_css %}
{% bootstrap_javascript %}
{% block content %}
<h1>글 수정</h1>

{% if request.path == '/articles/new/' %}
<h1> 생성 </h1>
{% endif %}

<form action="" method="POST">
    {% csrf_token %}
    {% bootstrap_form article_form %}
    {% bootstrap_button button_type='submit' content='OK' %}
    <input type="submit" value="수정">
</form>
{% endblock %}
```

```html
<!-- articles/templates/articles/forms.html -->
{% extends 'base.html' %}
{% load django_bootstrap5 %}
{% bootstrap_css %}
{% bootstrap_javascript %}
{% block content %}
<h1>글 수정</h1>

{{ request.resolver_match.url_name }}
{% if request.path == '/articles/new/' %}
<h1> 생성 </h1>
{% endif %}

<form action="" method="POST">
    {% csrf_token %}
    {% bootstrap_form article_form %}
    {% bootstrap_button button_type='submit' content='OK' %}
    <input type="submit" value="수정">
</form>
{% endblock %}
```
```html
{% extends 'base.html' %}
{% load django_bootstrap5 %}
{% bootstrap_css %}
{% bootstrap_javascript %}
{% block content %}

{% if request.resolver_match.url_name == 'new' %}
<h1> 생성 </h1>
{% else %}
<h1> 수정 </h1>
{% endif %}

<form action="" method="POST">
    {% csrf_token %}
    {% bootstrap_form article_form %}
    {% bootstrap_button button_type='submit' content='OK' %}
    <input type="submit" value="수정">
</form>
{% endblock %}
```

<br>

---
28. DateTime 바꾸기
- django DATETIME Filter
```html
{% extends 'base.html' %}
{% block content %}
<h1>{{ article.pk }}번</h1>
<h2>{{ article.created_at|date:'SHORT_DATETIME_FORMAT' }} | {{ article.updated_at|date:'y-m-d l' }}</h2>
<p>{{ article.content }}</p>

<a href="{% url 'articles:update' article.pk %}">글 수정</a>
<a href="{% url 'articles:index' %}">메인</a>
{% endblock %}
```

<br>

---
# 회원가입
29.  account 앱 생성
- `$ python manage.py startapp accounts`
```python
# pjt/settings.py
INSTALLED_APPS = [
    'articles',
    'accounts',
    'django_bootstrap5',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

<br>

---
30. django extensions
- `$ pip install django-extensions`
- `$ pip install ipython`
```python
# pjt/settings.py
INSTALLED_APPS = [
    'articles',
    'accounts',
    'django_bootstrap5',
    'django_extensions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```
- `$ python manage.py shell_plus`
- `$ Article.objects.create(title='제목1', content='내용1')`
- `$ User.objects.create(username='sun', password='1q2w3e4r')`
- `$ User.objects.create_user('kim', 'asdf@gmail.com', '1234')`
- `$ authenticate(username='kim', password='1234')`

<br>

---
31. account 사용 전 설정
- url 수정
```python
# pjt/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls')),
    path('accounts/', include('accounts.urls')),
]
```
<br>

- settings 수정
```python
# pjt/settings.py
AUTH_USER_MODEL = 'accounts.User'
```
<br>

- models 수정
```python
# accounts/models.py
# User model 직접 정의하는 것이 아닌 내장된 것을 활용
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass
# 프로젝트 초반에 작성하지 않으면 db.sqlite3 삭제 후 makemigrations => migrate
```
<br>

- `accounts` => `urls.py` 생성
```python
# account/urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
]
```
<br>

- views 수정
```python
# accounts/views.py
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def signup(request):
    form = UserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)
```
<br>

- templates 생성
```html
<!-- accounts/templates/accounts/signup.html -->
{% extends 'base.html' %}
{% block content %}
<h1>회원가입</h1>
{{ form.as_p }}
{% endblock %}
```
<br>

- templates 수정
```html
<!-- accounts/templates/accounts/signup.html -->
{% extends 'base.html' %}
{% load django_bootstrap5 %}
{% block content %}
<h1>회원가입</h1>
<form action="" method="POST">
    {% csrf_token %}
    {% bootstrap_form form %}
    {% bootstrap_button button_type='submit' content='OK' %}
</form>
{% endblock %}
```
<br>

- post 요청
```python
# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def signup(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = UserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)
```
- 여기까지만 하면 오류남
- auth안에 있는 User가 아닌, accounts에 정의한 User로 바꿔줘야 함

<br>

---
32. accounts의 User
- forms 생성
```python
# accounts/forms.py
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = '__all__'
```
<br>

- views 수정
```python
# accounts/views.py
from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm

# Create your views here.
def signup(request):
    if request.method =='POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)
```

<br>

---
33. 보여주고 싶은 form만 보여주기
- forms 수정
```python
# accounts/forms.py
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username',)
```
- articles forms: `froms.ModelForm`을 직접 상속해서 만듬
- accounts forms: `UsercreationForm`은 이미 만들어진 forms을 바탕으로 상속받아 커스텀하여 사용
- models도 forms와 마찬가지
- articles modles: `modles.Model`을 직접 상속해서 만듬
- accounts models: `AbstractUser`은 django 내부에서 어느정도 만들어진 models을 상속해서 만듦

<br>

---
34. admin 등록
```python
# accounts/admin.py
from django.contrib import admin
from .models import User

# Register your models here.
admin.site.register(User) 
```

<br>

---
35. User model => get_user_model
- User model: 변경가능한 모델, 상속받아서 만들었지만 기본 내장 설정은 auth User
- 즉, 직접 참조를 하지 않도록 함
- admin 수정
```python
# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from .models import User
from django.contrib.auth import get_user_model

# Register your models here.
admin.site.register(get_user_model(), UserAdmin)
```
<br>

- forms 수정
```python
# accounts/forms.py
from django.contrib.auth.forms import UserCreationForm
# from .models import User
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('username',)
```

<br>

---
36. profile
- urls 설정
```python
# account/urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('<int:pk>/', views.detail, name='detail'),
]
```
<br>

- views 추가
```python
# account/views.py
from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
# from .models import User
from django.contrib.auth import get_user_model

# Create your views here.
def signup(request):
    if request.method =='POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)

def detail(request, pk):
    user = get_user_model.objects.get(pk=pk)
    context = {
        'user': user
    }

    return render(request, 'accounts/detail.html', context)
```
- `from .models import User`: 사용 금지
- `from django.contrib.auth import get_user_model`: 사용
- articles views와 다른점: user class를 참조하는 방법만 다름
<br>

- templates 설정
```html
<!-- accounts/templates/accounts/detail.html -->
{% extends 'base.html' %}
{% block content %}
<h1>{{ user.username }}님의 프로필</h1>

{% endblock %}
```

<br>

---
# 로그인
37. login
- path 설정
```python
# accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('<int:pk>/', views.detail, name='detail'),
]
```
<br>

- views 수정
```python
# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model

# Create your views here.
def signup(request):
    if request.method =='POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)

def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    context = {
        'user': user
    }

    return render(request, 'accounts/detail.html', context)

def login(request):
    form  = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)
```
<br>

- login html 생성
```html
<!-- articles/templates/accounts/login.html -->
{% extends 'base.html' %}
{% load django_bootstrap5 %}
{% block content %}
<h1>로그인</h1>
<form action="" method="POST">
    {% csrf_token %}
    {% bootstrap_form form %}
    {% bootstrap_button button_type='submit' content='OK' %}
</form>
{% endblock %}
```
<br>

- 유효성 검사
```python
# accounts/views.py
def login(request):
    if request.method == 'POST':
        # AuthenticationForm은 ModelForm 아니다
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # form.save() # save 라는 명령어 없음: 모델 폼이 아니기 때문
            # 세션 저장
            # login 함수: request, user 객체를 인자로 받음
            # user 객체: form에서 인증된 유저 정보를 받을 수 있음
            auth_login(request, form.get_user())
            return redirect('articles:index')
        pass
    else:
        form  = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)
```
<br>

- 모든 페이지 로그인 정보 표시
```html
<!-- templates/base.html -->
{% load django_bootstrap5 %}
{% bootstrap_css %}
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body>
        <h1>{{ user }}</h1>
        <div class="container">
            {% block content %}
            {% endblock %}
        </div>
{% bootstrap_javascript %}
</body>
</html>
```
<br>

---
38.  로그인 회원가입 버튼
- base 수정
```html
<!-- templates/base.html -->
{% load django_bootstrap5 %}
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
        {% bootstrap_css %}
        {% block css %}{% endblock css %}
    </head>
    <body>
        <p>{{ user }}</p>
        <a href="{% url 'accounts:signup' %}">회원가입</a>
        <a href="{% url 'accounts:login' %}">로그인</a>


        <div class="container my-5">
            {% block content %}
            {% endblock %}
        </div>
{% bootstrap_javascript %}
</body>
</html>
```
<br>

---
39. 로그인 유무에 따른 회원가입 표시(분기 처리)
- base 수정
```html
<!-- templates/base.html -->
{% load django_bootstrap5 %}
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
        {% bootstrap_css %}
        {% block css %}{% endblock css %}
    </head>
    <body>
        {% comment %} request.user는 settings.py에 'django.contrib.auth.context_processors.auth', 때문에 user로 해도 괜찮다 {% endcomment %}
        {% if request.user.is_authenticated %}
            <span>{{ request.user }}</span>
            <a href="">로그아웃</a>
        {% else %}
            <a href="{% url 'accounts:signup' %}">회원가입</a>
            <a href="{% url 'accounts:login' %}">로그인</a>
        
        {% endif %}

        <div class="container my-5">
            {% block content %}
            {% endblock %}
        </div>
{% bootstrap_javascript %}
</body>
</html>
```
<br>

- index 수정
```html
<!-- articles/templates/articles/index.html -->
{% extends 'base.html' %}
{% load static %}
{% load django_bootstrap5 %}

{% block css %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
{% endblock %}


{% block content %}
<h1>게시판</h1>
{% if request.user.is_authenticated %}
    <a href="{% url 'articles:new' %}">글 작성</a>
{% endif %}
{% for article in articles %}
<h3><a href="{% url 'articles:detail' article.pk %}">{{ article.title }}</a></h3>
<p>{{ article.content }}</p>
<p>{{ article.created_at }} {{ article.updated_at }}</p>
<a href="{% url 'articles:delete' article.pk %}">글 삭제</a>
{% endfor %}
{% endblock %}
```
<br>

40. url 글 작성(create) 막기
- 백엔드로 막기(views)
- 기존 articles/views.py의 new
```python
# articles/views.py
def new(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():
            article_form.save()
            return redirect('articles:index')
    else:
        article_form = ArticleForm()
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/form.html', context)
```
<br>

- 수정 후 views.py의 new
```python
# articles/views.py
def new(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            article_form = ArticleForm(request.POST)
            if article_form.is_valid():
                article_form.save()
                return redirect('articles:index')
        else:
            article_form = ArticleForm()
        context = {
            'article_form': article_form
        }
        return render(request, 'articles/form.html', context)
    else:
        # 페이지 자체를 만들어서 return render 하는 방법
        # 혹은 로그인 페이지로 return redirect 하는 방법
        return redirect('accounts:login')
```
<br>

- 더 나은 방법 수정 전 views.py의 update
```python
# articles/views.py
def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, instance=article)
        if article_form.is_valid():
            article_form.save()
            return redirect('articles:detail', article.pk)
    else:
        article_form = ArticleForm(instance=article)
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/form.html', context)
```
<br>

- 수정 후 views.py의 update 
```python
# articles/views.py
from django.contrib.auth.decorators import login_required
@ login_required
def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, instance=article)
        if article_form.is_valid():
            article_form.save()
            return redirect('articles:detail', article.pk)
    else:
        article_form = ArticleForm(instance=article)
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/form.html', context)
```
- @ login_required: 실제 사용자가 로그인을 요구하는 상황에서 로그인 페이지로 보내주고, 이후에 행동을 view 함수(accounts/views.py에 login 함수)의 추가적인 처리로 해결

<br>

---
41.   GET 요청
- new 함수와 update 함수의 login 페이지로 부르는 것은 서로 url이 다름
- updat와 같은 url로 하고 싶다면 GET 요청으로 바꿔야 한다
- 기존 acoounts의 views.py
```python 
# accounts/views.py
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('articles:index')
        pass
    else:
        form  = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)
```
<br>

- 수정 후 account의 views.py
```python
# accounts/views.py
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            # request.GET.get('next') : articles/1/update
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            else:
                return redirect('articles:index')
        pass
    else:
        form  = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)
```
- 코드 줄이기
```python
# accounts/views.py
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'articles:index')
        pass
    else:
        form  = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)
```
<br>

- create 함수(new 함수) 줄이기
- if 문을 사용하지 않아도 되기 때문
- 기존 new 함수
```python
# articles/views.py
from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleForm

def new(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            article_form = ArticleForm(request.POST)
            if article_form.is_valid():
                article_form.save()
                return redirect('articles:index')
        else:
            article_form = ArticleForm()
        context = {
            'article_form': article_form
        }
        return render(request, 'articles/form.html', context)
    else:
        return redirect('accounts:login')
```
<br>

- 수정 후 new 함수
```python
# articles/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Article
from .forms import ArticleForm

@login_required 
def new(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():
            article_form.save()
            return redirect('articles:index')
    else:
        article_form = ArticleForm()
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/form.html', context)
```
<br>

---
# 로그아웃
42. logout
- url 설정
```python
# accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<int:pk>/', views.detail, name='detail'),
]
```
<br>

- views 설정
```python
# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout # logout 함수랑 겹치기 때문에 logout 이름을 auth_logout으로 바꿔줌
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm

def logout(request):
    auth_logout(request)
    return redirect('articles:index')
```
<br>

- base 수정(logout url 삽입)
```html
<!-- templates/base.html -->
{% load django_bootstrap5 %}
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
        {% bootstrap_css %}
        {% block css %}{% endblock css %}
    </head>
    <body>
        {% if request.user.is_authenticated %}
            <span>{{ request.user }}</span>
            <a href="{% url 'accounts:logout' %}">로그아웃</a>
        {% else %}
            <a href="{% url 'accounts:signup' %}">회원가입</a>
            <a href="{% url 'accounts:login' %}">로그인</a>
        
        {% endif %}

        <div class="container my-5">
            {% block content %}
            {% endblock %}
        </div>
{% bootstrap_javascript %}
</body>
</html>
```
<br>

---
43. 회원가입 후 자동로그인
- accounts views 수정
- 기존 signup views
```python
# accounts/veiws.py
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout # logout 함수랑 겹치기 때문에 logout 이름을 auth_logout으로 바꿔줌
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm

# Create your views here.
def signup(request):
    if request.method =='POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
            # 회원가입 후 로그인 페이지로 가려면 return redirect('articles:index')말고 return redirect('articles:login') 해주면 됨
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)
```
<br>

- 수정 후 sign views
```python
# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout # logout 함수랑 겹치기 때문에 logout 이름을 auth_logout으로 바꿔줌
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm

# Create your views here.
def signup(request):
    if request.method =='POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() # ModelForm의 save 메서드의 리턴값은 해당 모델의 인스턴스
            auth_login(request, user) # 로그인 함수 호출
            return redirect('articles:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)

def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    context = {
        'user': user
    }

    return render(request, 'accounts/detail.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'articles:index')
        pass
    else:
        form  = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('articles:index')
```
<br>

---
44. 회원가입 수정
- url 수정(update)
```python
# accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('update/', views.update, name='update'),
    path('<int:pk>/', views.detail, name='detail'),
]
```
<br>

- views 수정(update, CustomUserChangeForm)
```python
# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout # logout 함수랑 겹치기 때문에 logout 이름을 auth_logout으로 바꿔줌
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CustomUserChangeForm

def update(request):
    form = CustomUserChangeForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/update.html', context)
```
- 여기까지 하면 수정이지만 실제론 비어있다 `form = CustomUserChangeForm()`를 수정해줘야함

<br>

- views 수정
```python
# accounts/views.py
def update(request):
    form = CustomUserChangeForm(instance=request.user)
    # 기존 값을 로그인한 유저 instance=request.user
    context = {
        'form': form
    }
    return render(request, 'accounts/update.html', context)
```

<br>

- html 생성
```html
<!-- accounts/templates/accounts/update.html -->
{% extends 'base.html' %}
{% load django_bootstrap5 %}
{% block content %}
<h1>프로필 업데이트</h1>
<form action="" method="POST">
    {% csrf_token %}
    {% bootstrap_form form %}
    {% bootstrap_button button_type='submit' content='OK' %}
</form>
{% endblock %}
```
<br>

- form 수정(UserChangeForm Custom)
```python
# accounts/forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from .models import User
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('username',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = '__all__'

# Article Create/Update: ArticleForm을 같이 사용했는데,
# User Create/Update: Form을 다르게 사용하는가?

# 사용자는 비밀번호가 다름
# User Create: 비밀번호 2개를 받아서 일치하는 로직이 포함됨 => UserCreationForm
# User Update: 비밀번호 2개를 받을 필요가 있나?, 구성 자체가 다른거 같음, 비밀번호는 그대로 입력해서 주면 됨?, 구성이 다를수도?
```
<br>

- form 수정(fields)
```python
# accounts/forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from .models import User
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('username',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email')
```

<br>

---
45. 회원가입 내용 받기
- view 수정(update)
```python
# accounts/views.py
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:detail')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/update.html', context)
```
- 여기까지 하면 오류 남: `NoReverseMatch`
- url 변수화 해놓은 것을 path로 변환하는 과정에서 매치되지 않음


<br>

- view 수정(request.user.pk)
```python
# accounts/views.py
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:detail', request.user.pk)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/update.html', context)
```
- 로그인한 user의 pk값 넣어줌

<br>

- html 수정(기존 html)
```html
<!-- accounts/templates/accounts/detail.html -->
{% extends 'base.html' %}
{% block content %}
<h1>{{ user.username }}님의 프로필</h1>

{% endblock %}
```

<br>

- html 수정
  - email, first_name 정보 입력
```html
<!-- accounts/templates/accounts/detail.html -->
{% extends 'base.html' %}
{% block content %}
<h1>{{ user.username }}님의 프로필</h1>
<p>{{ user.email }} | {{ user.first_name }}</p>
{% endblock %}
```
<br>

---
46. 이름 순서 바꾸기
- model 수정
- 기존 accounts models
```python
# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass
```

<br>

- 수정된 accounts models
```python
# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    @property
    def full_name(self):
        return f'{self.last_name}{self.first_name}'
```
- 클래스의 값들을 조합해서 보여줄때 models에 정의하면 됨

<br>

- detail 페이지 수정(full_name)
```html
<!-- accounts/templates/accounts/detail.html -->
{% extends 'base.html' %}
{% block content %}
<h1>{{ user.username }}님의 프로필</h1>
<p>{{ user.email }} | {{ user.full_name }}</p>
{% endblock %}
```
- 여기까지하면 로그인한 상태에서 update는 되지만, 로그아웃한 상태에서 update는 오류가 남(views.py)
- 로그인을 해야 접속 가능하도록 `login_required` 해주면 됨

<br>

---
47. logout 상태의 update
- view 수정(login_required)
```python
# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CustomUserChangeForm

@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:detail', request.user.pk)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/update.html', context)
```
- `login_required`를 하면 `accounts/update`(프로필 수정 페이지)에 들어갈 수 없고, 로그인 페이지로 들어감
- `login_required` 필요한 상황: 로그인이 필요할 때, `request.user`로 유저객체를 사용하는 `view 함수`에서는 되도록 사용(: 안할시 오류가 나기 때문)


<br>

---
# 이미지 저장
48. Pillow 설치
- pillow: 이미지 관리하기 위해 설치(python image 라이브러리)
```bash
$ pip install Pillow
```
<br>

```bash
$ python3 -m pip install --upgrade pip
```
[pillow 문서](https://pillow.readthedocs.io/en/stable/installation.html)

<br>

---
49. articles 설정
- model 수정
```python
# articles/models.py
from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/', blank=True)
    # blank=True: 이미지가 항상 업로드 되는건 아니기 떄문에 넣어줌
```
<br>

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```
<br>

- form 수정
```python
# articles/forms.py
from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image']
```
- 게시글 저장 O, 하지만 image 받지 못하는 상황

<br>

- html 수정(enctype)
```python
# articles/templates/articles/form.html
{% extends 'base.html' %}
{% load django_bootstrap5 %}
{% bootstrap_css %}
{% bootstrap_javascript %}
{% block content %}

{% if request.resolver_match.url_name == 'new' %}
<h1> 생성 </h1>
{% else %}
<h1> 수정 </h1>
{% endif %}

<form action="" method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    {% bootstrap_form article_form %}
    {% bootstrap_button button_type='submit' content='OK' %}
    <input type="submit" value="수정">
</form>
{% endblock %}
```

<br>

- html 삭제
    - `create.html`: 더 이상 사용하지 않기 때문에 삭제해도됨

<br>

- view 수정(request.FILES)
```python
# articles/views.py
@login_required 
def new(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
            article_form.save()
            return redirect('articles:index')
    else:
        article_form = ArticleForm()
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/form.html', context)
```
- `images`폴더에 image가 들어와 있음(즉, 이미지를 서버에 저장받을 수 있다)

<br>

- form으로 file 받을 때 2가지 설정
  - html form 자체에서 file 받는 옵션
  - view에서 file을 별도로 model form에 넣어서 줌

<br>

---
49. image 보여주기
- html 수정(article.image.url)
```html
<!-- accounts/templates/accounts/detail.html -->
{% extends 'base.html' %}
{% block content %}
<h1>{{ article.pk }}번</h1>
<h2>{{ article.created_at|date:'SHORT_DATETIME_FORMAT' }} | {{ article.updated_at|date:'y-m-d l' }}</h2>
<p>{{ article.content }}</p>
<img src="{{ article.image.url }}" alt="{{ article.image }}" width="400" height="300">
<a href="{% url 'articles:update' article.pk %}">글 수정</a>
<a href="{% url 'articles:index' %}">메인</a>
{% endblock %}
```

- settings 설정
```python
# pjt/settings.py
MIDEA_ROOT = BASE_DIR / 'images'
MIDEA_URL = '/midia/'
```

- url 설정(settings, static)
```python
# pjt/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls')),
    path('accounts/', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

<br>

---
50. image resizing
- django-imagekit
```bash
$ pip install django-imagekit
```
<br>

- settings 설정
```python
# pjt/settings.py
INSTALLED_APPS = [
    'articles',
    'accounts',
    'django_bootstrap5',
    'django_extensions',
    'imagekit',
    'django.contrib.admin', # 관리자
    'django.contrib.auth', # 유저/인증
    'django.contrib.contenttypes',
    'django.contrib.sessions', # 세션 관리
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

- model 설정(imagekit)
- 기존 model
```python
# articles/models.py
from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/', blank=True)
```
<br>

- 변경 후 model
```python
# articles/models.py
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = ProcessedImageField(upload_to='images/', blank=True,
                                processors=[ResizeToFill(400, 300)],
                                format='JPEG',
                                options={'quality': 80})
```

<br>

---
51. image 분기처리
- html 수정
```html
<!-- articles/templates/articles/detail.html -->
{% extends 'base.html' %}
{% block content %}
<h1>{{ article.pk }}번</h1>
<h2>{{ article.created_at|date:'SHORT_DATETIME_FORMAT' }} | {{ article.updated_at|date:'y-m-d l' }}</h2>
<p>{{ article.content }}</p>
{% if article.image %}
    <img src="{{ article.image.url }}" alt="{{ article.image }}" width="400" height="300">
{% endif %}
<a href="{% url 'articles:update' article.pk %}">글 수정</a>
<a href="{% url 'articles:index' %}">메인</a>
{% endblock %}
```

<br>

---
52. 글 수정(image)
- view 수정
- 기존 views(update)
```python
# articles/views.py
@ login_required
def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, instance=article)
        if article_form.is_valid():
            article_form.save()
            return redirect('articles:detail', article.pk)
    else:
        article_form = ArticleForm(instance=article)
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/form.html', context)
```
<br>

- 변경 후 views(request.FILES)
```python
# articles/views.py
@ login_required
def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES, instance=article)
        if article_form.is_valid():
            article_form.save()
            return redirect('articles:detail', article.pk)
    else:
        article_form = ArticleForm(instance=article)
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/form.html', context)
```

<br>

---
53. html 수정
- base 수정(navbar)
```html
<!-- templates/base.html -->
{% load django_bootstrap5 %}
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
        {% bootstrap_css %}
        {% block css %}{% endblock css %}
    </head>
    <body>
        <nav class="navbar navbar-expand-lg bg-primary navbar-dark">
            <div class="container-fluid">
              <a class="navbar-brand" href="#">Navbar</a>
              <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
              </button>
              <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                  <li class="nav-item">
                    <a class="nav-link active" aria-current="page" href="{% url 'articles:index' %}">Home</a>
                  </li>
                    {% if request.user.is_authenticated %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'accounts:detail' request.user.pk %}">{{ request.user }}</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'accounts:logout' %}">로그아웃</a>
                        </li>
                    {% else %}
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'accounts:signup' %}">회원가입</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{% url 'accounts:login' %}">로그인</a>
                        </li>
                    {% endif %}
                </ul>
              </div>
            </div>
          </nav>

        <div class="container my-5">
            {% block content %}
            {% endblock %}
        </div>
{% bootstrap_javascript %}
</body>
</html>
```
- 이후 bootstrap 사용하여 꾸미기

<br>

---
54. message
- settings 설정
```python
# pjt/settings.py
# message framework
# https://docs.djangoproject.com/en/4.1/ref/contrib/messages/
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
```
<br>

- view 설정(messages)
```python
# articles/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Article
from .forms import ArticleForm

@login_required 
def new(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
            article_form.save()
            messages.success(request, '글 작성 완료')
            return redirect('articles:index')
    else:
        article_form = ArticleForm()
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/form.html', context)

@ login_required
def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES, instance=article)
        if article_form.is_valid():
            article_form.save()
            messages.success(request, '글 수정 완료')
            return redirect('articles:detail', article.pk)
    else:
        article_form = ArticleForm(instance=article)
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/form.html', context)
```
<br>

- base html 추가(message)
```html
<!-- templates/base.html -->
          {% if messages %}
            <ul class="messages">
            {% for message in messages %}
              <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
            {% endfor %}
            </ul>
          {% endif %}
```
<br>

- base html 수정
```html
<!-- templates/base.html -->
          {% if messages %}
            {% for message in messages %}
              <div class="alert alert-{{ message.tags }}">
                {{ message }}
              </div>
            {% endfor %}
          {% endif %}

```

<br>

---
55. Warning(message)
- view 수정
```python
# accounts/views.py
from django.contrib import messages

def logout(request):
    auth_logout(request)
    messages.warning(request, '로그아웃!')
    return redirect('articles:index')
```

<br>

---
# COMMENT
56. Comment
- model 설정
```python
# articles/models.py
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = ProcessedImageField(upload_to='images/', blank=True,
                                processors=[ResizeToFill(1200, 960)],
                                format='JPEG',
                                options={'quality': 80})

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
```
- 혹은(`Article` 문자열로 대체 가능[순서 때문])
```python
# articles/models.py
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.db import models

# Create your models here.
class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)

class Article(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = ProcessedImageField(upload_to='images/', blank=True,
                                processors=[ResizeToFill(1200, 960)],
                                format='JPEG',
                                options={'quality': 80})
```
<br>

- admin 설정(comment)
```python
# articles/admin.py
from django.contrib import admin
from .models import Article, Comment

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')

admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
```
<br>

- 댓글 정보 포함
```python
# articles/admin.py
from django.contrib import admin
from .models import Article, Comment

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'created_at', 'article')

admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
```
<br>

- 확인
```bash
$ python manage.py shell_plus
Article.objects.all()
Article.objects.create(title='제목1', content='내용1')
article = Article.objects.create(title='제목1', content='내용1')
article

# 게시글 12번에 내용이 111인 댓글을 생성하는 코드 작성
comment = Comment.objects.create(content='111', article=article)
comment

comment.article
# <Article: Article object (12)>

comment.article.id
# 12

comment = Comment.objects.create(content='111', article_id=12)
# 필드 값만 기억해주면 위처럼 입력해도 상관없다

# 12번 게시글의 모든 댓글을 알고 싶을 때
Comment.objects.filter(article_id=12) # 직접 참조
article.comment_set.all() # 역참조
# 두 개의 결과 같음
```

<br>

---
57. Comment 목록
- html 수정(for문 활용 comment)
```html
<!-- articles/templates/articles/detail.html -->
{% extends 'base.html' %}
{% block content %}
<h1>{{ article.pk }}번</h1>
<h2>{{ article.created_at|date:'SHORT_DATETIME_FORMAT' }} | {{ article.updated_at|date:'y-m-d l' }}</h2>
<p>{{ article.content }}</p>
{% if article.image %}
    <img src="{{ article.image.url }}" alt="{{ article.image }}" width="400" height="300">
{% endif %}
<a href="{% url 'articles:update' article.pk %}">글 수정</a>

<h4 class="my-3">댓글</h4>
<hr>
{% for comment in article.comment_set.all %}
    <p>{{ comment.content }}</p>
    <hr>
{% endfor %}

<a href="{% url 'articles:index' %}">메인</a>
{% endblock %}
```
- for문에 `()`가 빠져있는게 아닌

<br>

- 동일한 코드를 만들어보면(`'comment': article.comment_set.all(),`)
- view에서 변수 넘기기
```python
# articles/views.py
def detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    context = {
        'article': article,
        'comments': article.comment_set.all(),
    }
    return render(request, 'articles/detail.html', context)
```
- `article.comment_set.all` => `comments`
```html
<!-- articles/templates/articles/detail.html -->
{% extends 'base.html' %}
{% block content %}
<h1>{{ article.pk }}번</h1>
<h2>{{ article.created_at|date:'SHORT_DATETIME_FORMAT' }} | {{ article.updated_at|date:'y-m-d l' }}</h2>
<p>{{ article.content }}</p>
{% if article.image %}
    <img src="{{ article.image.url }}" alt="{{ article.image }}" width="400" height="300">
{% endif %}
<a href="{% url 'articles:update' article.pk %}">글 수정</a>

<h4 class="my-3">댓글</h4>
<hr>
{% for comment in comments %}
    <p>{{ comment.content }}</p>
    <hr>
{% endfor %}

<a href="{% url 'articles:index' %}">메인</a>
{% endblock %}
```
<br>

- comment 없을 때(empty)
```html
<!-- articles/templates/articles/detail.html -->
{% extends 'base.html' %}
{% block content %}
<h1>{{ article.pk }}번</h1>
<h2>{{ article.created_at|date:'SHORT_DATETIME_FORMAT' }} | {{ article.updated_at|date:'y-m-d l' }}</h2>
<p>{{ article.content }}</p>
{% if article.image %}
    <img src="{{ article.image.url }}" alt="{{ article.image }}" width="400" height="300">
{% endif %}
<a href="{% url 'articles:update' article.pk %}">글 수정</a>

<h4 class="my-3">댓글</h4>
<hr>
{% for comment in comments %}
    <p>{{ comment.content }}</p>
    <hr>
{% empty %}
    <p>댓글 없엉 ㅠㅠ</p>
{% endfor %}

<a href="{% url 'articles:index' %}">메인</a>
{% endblock %}
```

<br>

---
58. comment form
- form 설정(Comment)
```python
# articles/forms.py
from django import forms
from .models import Article, Comment

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
# comment form을 넘겨주는 곳은 따로 존재하는 것이 아닌 articles/views.py의 detail 함수
```
<br>

- view 설정(Comment)
```python
# articles/views.py
from .forms import ArticleForm, CommentForm

def detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    comment_form = CommentForm()
    context = {
        'article': article,
        'comments': article.comment_set.all(),
        'comment_form': comment_form,
    }
    return render(request, 'articles/detail.html', context)
```
<br>

- html 수정(bootstrap, comment_form)
```html
<!-- articles/templates/articles/detail.html -->
{% extends 'base.html' %}
{% load django_bootstrap5 %}
{% block content %}
<h1>{{ article.pk }}번</h1>
<h2>{{ article.created_at|date:'SHORT_DATETIME_FORMAT' }} | {{ article.updated_at|date:'y-m-d l' }}</h2>
<p>{{ article.content }}</p>
{% if article.image %}
    <img src="{{ article.image.url }}" alt="{{ article.image }}" width="400" height="300">
{% endif %}
<a href="{% url 'articles:update' article.pk %}">글 수정</a>

<h4 class="my-3">댓글</h4>
<form action="">
    {% bootstrap_form comment_form layout='inline' %}
    <!--layout='inline': 라벨 사라짐 -->
    {% bootstrap_button button_type='submit' content='OK' %}
</form>

<hr>
{% for comment in comments %}
    <p>{{ comment.content }}</p>
    <hr>
{% empty %}
    <p>댓글 없엉 ㅠㅠ</p>
{% endfor %}

<a href="{% url 'articles:index' %}">메인</a>
{% endblock %}
```
<br>

---
59. comment 처리
- url 설정
```python
# articles/urls.py
from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('new/', views.new, name='new'),
    path('<int:article_pk>/detail/', views.detail, name='detail'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/comments/', views.comment_create, name='comment_create'),
]
```
<br>

- view 설정
```python
# articles/views.py
def comment_create(request, pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)

    if comment_form.is_valid():
        comment_form.save()
    return redirect('articles:detail', article.pk)
```
<br>

- html 수정(`<form action="{% url 'articles:comment_create' article.pk %}" method="POST">`, `csrf_token`)
```html
<!-- articles/templates/articles/detail.html -->
{% extends 'base.html' %}
{% load django_bootstrap5 %}
{% block content %}
<h1>{{ article.pk }}번</h1>
<h2>{{ article.created_at|date:'SHORT_DATETIME_FORMAT' }} | {{ article.updated_at|date:'y-m-d l' }}</h2>
<p>{{ article.content }}</p>
{% if article.image %}
    <img src="{{ article.image.url }}" alt="{{ article.image }}" width="400" height="300">
{% endif %}
<a href="{% url 'articles:update' article.pk %}">글 수정</a>

<h4 class="my-3">댓글</h4>
<form action="{% url 'articles:comment_create' article.pk %}" method="POST">
    {% csrf_token %}
    {% bootstrap_form comment_form layout='inline' %}
    {% bootstrap_button button_type='submit' content='OK' %}
</form>

<hr>
{% for comment in comments %}
    <p>{{ comment.content }}</p>
    <hr>
{% empty %}
    <p>댓글 없엉 ㅠㅠ</p>
{% endfor %}

<a href="{% url 'articles:index' %}">메인</a>
{% endblock %}
```
- NOT NULL 제약조건 때문에 오류남

<br>

- view 수정
```python
# articles/views.py
def comment_create(request, pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)

    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        # save하기 전 commit=False로 멈춤

        comment.article = article
        comment.save()
        # return한 객체를 조작해서 저장
    return redirect('articles:detail', article.pk)
```
- DB에 직접 저장하지말고 객체를 주면 넣을 값들 넣고 저장(save) 호출
- `comment_form`: CommentForm의 instance(모델폼 인스턴스)
- `comment`: Comment 클래스의 instance
- 모델폼의 save 메서드는 return 값이 해당 모델의 인스턴스이다

<br>

---
# 1:1 - 1:N - N:M
60. user class 가져오기
- model 설정(settings, user)
```python
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from django.db import models

# Create your models here.
from django.conf import settings
# settings 가져옴

class Article(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = ProcessedImageField(upload_to='images/', blank=True,
                                processors=[ResizeToFill(1200, 960)],
                                format='JPEG',
                                options={'quality': 80})
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 위의 1줄: get user 모델 사용하는 것과 차이 없음

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
```
<br>

- `$ python manage.py makemigrations`
```terminal
You are trying to add a non-nullable field 'user' to article without a default; we can't do that (the database needs something to populate existing rows).
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit, and let me add a default in models.py
```
- 1번 선택(1 입력) => 3번 유저 입력(3 입력)

<br>

- `$ python manage.py migrate`
- 여기까지하고 글 작성시 오류남(`NOT NULL constraint failed: articles_article.user_id
`)
- user_id에 NULL 값이 있을 수 없기 때문
- db.splite3: `articles_article`: 테이블 이름 | `user_id`: 필드 이름

<br>

---
61.  1:N
- model 수정
- 기존 model
```python
# articles/forms.py
from django import forms
from .models import Article, Comment

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
```
<br>

- 수정 후 model(ArticleForm)
```python
# articles/forms.py
from django import forms
from .models import Article, Comment

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
```
- 글쓰기에서 user 선택 가능
- 하지만 User 선택하는건 안됨(`__all__`이 좋은게 아님)
- 코드 변경해줘야함(`articles/views.py`에 `create 함수`)

<br>

- view 수정
- 기존 view
```python
# articles/views.py
@login_required 
def new(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
            article_form.save()
            messages.success(request, '글 작성 완료')
            return redirect('articles:index')
    else:
        article_form = ArticleForm()
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/form.html', context)
```
<br>

- 수정 후 views(commit=False)
```python
# articles/views.py
@login_required 
def new(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
            article = article_form.save(commit=False)
            # 로그인한 유저 => 작성자임
            article.user = request.user
            article.save()
            messages.success(request, '글 작성 완료')
            return redirect('articles:index')
    else:
        article_form = ArticleForm()
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/form.html', context)
```
### User 정보 어떻게 넣을까?
- views.py 함수 정의된 곳에서, 내가 사용자로부터(요청) 받을 수 있는 정보:
- request.POST / request.GET / URL(variable routing)

<br>

- 사용자는 어떻게 요청으로 서버에 값을 전달?:
- request => Form(Form에서 값 입력해줘)
- URL => 내가 선택한 길(게시글 보기: 버톤 선택시 URL 값 넣어놔둠)

<br>

- html 수정(article.user)
```html
<!-- articles/templates/articles/detail.html -->
{% extends 'base.html' %}
{% load django_bootstrap5 %}
{% block content %}
<h1>{{ article.pk }}번</h1>

<h3>{{ article.user }}</h3>

<h2>{{ article.created_at|date:'SHORT_DATETIME_FORMAT' }} | {{ article.updated_at|date:'y-m-d l' }}</h2>
<p>{{ article.content }}</p>
{% if article.image %}
    <img src="{{ article.image.url }}" alt="{{ article.image }}" width="400" height="300">
{% endif %}
<a href="{% url 'articles:update' article.pk %}">글 수정</a>

<h4 class="my-3">댓글</h4>
<form action="{% url 'articles:comment_create' article.pk %}" method="POST">
    {% csrf_token %}
    {% bootstrap_form comment_form layout='inline' %}
    {% bootstrap_button button_type='submit' content='OK' %}
</form>

<hr>
{% for comment in comments %}
    <p>{{ comment.content }}</p>
    <hr>
{% empty %}
    <p>댓글 없엉 ㅠㅠ</p>
{% endfor %}

<a href="{% url 'articles:index' %}">메인</a>
{% endblock %}
```
<br>

- html 수정(`article.user.username`)
```html
<!-- articles/templates/articles/index.html -->
{% extends 'base.html' %}
{% load static %}
{% load django_bootstrap5 %}

{% block css %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
{% endblock %}


{% block content %}
<h1>게시판</h1>
{% if request.user.is_authenticated %}
    <a class="btn btn-primary my-3" href="{% url 'articles:new' %}">글 작성</a>
{% endif %}
{% for article in articles %}
<h3><a href="{% url 'articles:detail' article.pk %}">{{ article.title }}</a></h3>
<p>{{ article.content }}</p>
<p>{{ article.created_at }} {{ article.updated_at }}</p>

<p>{{ article.user.username }}</p>

<a href="{% url 'articles:delete' article.pk %}">글 삭제</a>
{% endfor %}
{% endblock %}
```

<br>

---
62. User가 작성한 글 확인
- html 수정(`user.article_set.all`)
```html
<!-- accounts/templates/accounts/detail.html -->
{% extends 'base.html' %}
{% block content %}
<h1>{{ user.username }}님의 프로필</h1>
<p>{{ user.email }} | {{ user.full_name }}</p>

<h3>작성한 글</h3>
{% for article in user.article_set.all %}
<a href="{% url 'articles:detail' article.pk %}">{{ article.title }}</a>
{% endfor %}

{% endblock %}
```
<br>

- html 수정(`article.user.id`, `article.user.username`)
- detail 페이지에서 유저 이름 선택시 해당 유저 페이지로 가기
```html
<!-- articles/templates/articles/detail.html -->
{% extends 'base.html' %}
{% load django_bootstrap5 %}
{% block content %}
<h2>{{ article.title }}</h2>

<p>{{ article.pk }}번</p>
<h3><a href="{% url 'accounts:detail' article.user.id %}">{{ article.user.username }}</a></h3>

<p>{{ article.created_at|date:'SHORT_DATETIME_FORMAT' }} | {{ article.updated_at|date:'y-m-d l' }}</p>
<p>{{ article.content }}</p>
{% if article.image %}
    <img src="{{ article.image.url }}" alt="{{ article.image }}" width="400" height="300">
{% endif %}
<a href="{% url 'articles:update' article.pk %}">글 수정</a>

<h4 class="my-3">댓글</h4>
<form action="{% url 'articles:comment_create' article.pk %}" method="POST">
    {% csrf_token %}
    {% bootstrap_form comment_form layout='inline' %}
    {% bootstrap_button button_type='submit' content='OK' %}
</form>

<hr>
{% for comment in comments %}
    <p>{{ comment.content }}</p>
    <hr>
{% empty %}
    <p>댓글 없엉 ㅠㅠ</p>
{% endfor %}

<a href="{% url 'articles:index' %}">메인</a>
{% endblock %}
```
<br>

- html 수정
- 유저가 작성한 글(몇번째 글인지) 순서대로 보여주기(`forloop.counter`)
- 총 몇개의 글이 작성되었는지(`user.article_set.count`)
```html
<!-- accounts/templates/accounts/detail.html -->
{% extends 'base.html' %}
{% block content %}
<h1>{{ user.username }}님의 프로필</h1>
<p>{{ user.email }} | {{ user.full_name }}</p>

<h3>작성한 글</h3>
<p class="text-muted">{{ user.article_set.count }}개 작성 완료</p>
{% for article in user.article_set.all %}
<p>
    {{ forloop.counter }}
    <a href="{% url 'articles:detail' article.pk %}">{{ article.title }}</a>
</p>
{% endfor %}

{% endblock %}
```
<br>

- html 수정(`url 'accounts:detail' article.user.id``)
```html
<!-- accounts/templates/accounts/index.html -->
{% extends 'base.html' %}
{% load static %}
{% load django_bootstrap5 %}

{% block css %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
{% endblock %}


{% block content %}
<h1>게시판</h1>
{% if request.user.is_authenticated %}
    <a class="btn btn-primary my-3" href="{% url 'articles:new' %}">글 작성</a>
{% endif %}
{% for article in articles %}
<h3><a href="{% url 'articles:detail' article.pk %}">{{ article.title }}</a></h3>
<p>{{ article.content }}</p>
<p>{{ article.created_at }} {{ article.updated_at }}</p>

{% comment %} <p class="text-muted">{{ article.user.username }}</p> {% endcomment %}
<p class="text-muted"><a href="{% url 'accounts:detail' article.user.id %}">{{ article.user.username }}</a></p>


<a href="{% url 'articles:delete' article.pk %}">글 삭제</a>
{% endfor %}
{% endblock %}
```

<br>

---
63. 본인 글만 수정하기
- html 수정(`request.user == article.user`)
```html
<!-- accounts/templates/accounts/detail.html -->
{% extends 'base.html' %}
{% load django_bootstrap5 %}
{% block content %}
<h2>{{ article.title }}</h2>
<p>{{ article.pk }}번</p>
<h3><a href="{% url 'accounts:detail' article.user.id %}">{{ article.user.username }}</a></h3>
<p>{{ article.created_at|date:'SHORT_DATETIME_FORMAT' }} | {{ article.updated_at|date:'y-m-d l' }}</p>
<p>{{ article.content }}</p>
{% if article.image %}
    <img src="{{ article.image.url }}" alt="{{ article.image }}" width="400" height="300">
{% endif %}

{% if request.user == article.user %}
<p>
    <a href="{% url 'articles:update' article.pk %}">글 수정</a>
</p>
{% endif %}

<h4 class="my-3">댓글</h4>
<form action="{% url 'articles:comment_create' article.pk %}" method="POST">
    {% csrf_token %}
    {% bootstrap_form comment_form layout='inline' %}
    {% bootstrap_button button_type='submit' content='OK' %}
</form>

<hr>
{% for comment in comments %}
    <p>{{ comment.content }}</p>
    <hr>
{% empty %}
    <p>댓글 없엉 ㅠㅠ</p>
{% endfor %}

<a href="{% url 'articles:index' %}">메인</a>
{% endblock %}
```
- 여기까지해도 url 검색시 들어올 수 있음
- view에서 막아줘야 함

<br>

- view 수정
- 기존 update 함수
```python
# articles/views.py
from django.contrib.auth.decorators import login_required
@ login_required
def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES, instance=article)
        if article_form.is_valid():
            article_form.save()
            messages.success(request, '글 수정 완료')
            return redirect('articles:detail', article.pk)
    else:
        article_form = ArticleForm(instance=article)
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/form.html', context)
```
<br>

- 수정 후 update 함수(`request.user == article.user`)
```python
# article/views.py
from django.contrib.auth.decorators import login_required
@ login_required
def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.user == article.user:
        if request.method == 'POST':
            article_form = ArticleForm(request.POST, request.FILES, instance=article)
            if article_form.is_valid():
                article_form.save()
                messages.success(request, '글 수정 완료')
                return redirect('articles:detail', article.pk)
        else:
            article_form = ArticleForm(instance=article)
        context = {
            'article_form': article_form
        }
        return render(request, 'articles/form.html', context)
```
<br>

- 수정 후 update 함수(`HttpResponseForbidden`)
- url로 다른 유저 update 들어갈 경우 view에서 막는 방법 1
```python
# article/views.py
from django.contrib.auth.decorators import login_required
@ login_required
def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.user == article.user:
        if request.method == 'POST':
            article_form = ArticleForm(request.POST, request.FILES, instance=article)
            if article_form.is_valid():
                article_form.save()
                messages.success(request, '글 수정 완료')
                return redirect('articles:detail', article.pk)
        else:
            article_form = ArticleForm(instance=article)
        context = {
            'article_form': article_form
        }
        return render(request, 'articles/form.html', context)
    else:
        # 작성자 아닐때
        # 1. error message
        # 403 메시지
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden()
```
<br>

- 수정 후 update 함수(`redirect`, `message`)
- url로 다른 유저 update 들어갈 경우 view에서 막는 방법 2
```python
# article/views.py
from django.contrib.auth.decorators import login_required
@ login_required
def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.user == article.user:
        if request.method == 'POST':
            article_form = ArticleForm(request.POST, request.FILES, instance=article)
            if article_form.is_valid():
                article_form.save()
                messages.success(request, '글 수정 완료')
                return redirect('articles:detail', article.pk)
        else:
            article_form = ArticleForm(instance=article)
        context = {
            'article_form': article_form
        }
        return render(request, 'articles/form.html', context)
    else:
        # 2. flash message 사용
        messages.warning(request, '작성자만 작성 가능!')
        return redirect('articles:detail', article.pk)
```

<br>

---
# comment user
63. comment user
- model 수정(`user`)
```python
# articles/models.py
class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # user: settings.AUTH_USER_MODEL에 정의된 accounts 앱의 user라는 class 의미함
    # 문자열로 들어갈 수 있음: 문자열을 settings에서 가져옴
    # comment는 user을 직접참조
    # user는 comment를 역참조: user.comment_set.all()
```
<br>

```bash
$ python3 manage.py makemigrations
```
- You are trying to add a non-nullable field 'user' to comment without a default; we can't do that (the database needs something to populate existing rows).
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit, and let me add a default in models.py
- 1 입력 => 3 입력(3번 유저로)
```bash
$ python3 manage.py migrate
```
- 댓글 입력시 `NOT NULL constraint failed: articles_comment.user_id` 오류 남
- `comment` 모델은 `user_id`필드가 생겨있기 때문

<br>

- view 수정(`comment.user = request.user`)
- 로그인이 필요함
```python
# articles/views.py
@login_required
# POST 요청으로 보내서 url로 접속할 방법이 없지만, 그러지 않고 POST요청으로 보낼 수 있기 때문에 login_required 넣어줌
def comment_create(request, pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)

    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article = article

        comment.user = request.user

        comment.save()
    return redirect('articles:detail', article.pk)
```
<br>

- html 수정(`comment.user.username`, `request.user.is_authenticated`)
- 누가 작성한 댓글인지 확인, 로그인한 유저만 댓글작성 가능
```html
<!-- accounts/templates/accounts/detail.html -->
{% extends 'base.html' %}
{% load django_bootstrap5 %}
{% block content %}
<h2>{{ article.title }}</h2>
<p>{{ article.pk }}번</p>
<h3><a href="{% url 'accounts:detail' article.user.id %}">{{ article.user.username }}</a></h3>
<p>{{ article.created_at|date:'SHORT_DATETIME_FORMAT' }} | {{ article.updated_at|date:'y-m-d l' }}</p>
<p>{{ article.content }}</p>
{% if article.image %}
    <img src="{{ article.image.url }}" alt="{{ article.image }}" width="400" height="300">
{% endif %}

{% if request.user == article.user %}
<p>
    <a href="{% url 'articles:update' article.pk %}">글 수정</a>
</p>
{% endif %}

<h4 class="my-3">댓글</h4>

{% if request.user.is_authenticated %}
<form action="{% url 'articles:comment_create' article.pk %}" method="POST">
    {% csrf_token %}
    {% bootstrap_form comment_form layout='inline' %}
    {% bootstrap_button button_type='submit' content='OK' %}
</form>
{% endif %}


<hr>
{% for comment in comments %}

    <p>{{ comment.user.username }} | {{ comment.content }}</p>

    <hr>
{% empty %}
    <p>댓글 없엉 ㅠㅠ</p>
{% endfor %}

<a href="{% url 'articles:index' %}">메인</a>
{% endblock %}
```
<br>

- html 수정
- user.profile 페이지 반반 나눠 표현
- 기존 html
```html
<!-- accounts/templates/accounts/detail.html -->
{% extends 'base.html' %}
{% block content %}
<h1>{{ user.username }}님의 프로필</h1>
<p>{{ user.email }} | {{ user.full_name }}</p>

<h3>작성한 글</h3>
<p class="text-muted">{{ user.article_set.count }}개 작성 완료</p>
{% for article in user.article_set.all %}
<p>
    {{ forloop.counter }}
    <a href="{% url 'articles:detail' article.pk %}">{{ article.title }}</a>
</p>
{% endfor %}

{% endblock %}
```
<br>

- 수정 후 html
- 프로필 페이지에 유저가 작성한 글과 댓글 표시
- 댓글 클릭시 해당 글로 이동(`articles:detail' comment.article.id`, `articles:detail' comment.article.pk` 둘 다 가능)
```html
<!-- accounts/templates/accounts/detail.html -->
{% extends 'base.html' %}
{% block content %}
<h1>{{ user.username }}님의 프로필</h1>
<p>{{ user.email }} | {{ user.full_name }}</p>
<div class="row">
    <div class="col-6">
        <h3>작성한 글</h3>
        <p class="text-muted">{{ user.article_set.count }}개 작성 완료</p>
        {% for article in user.article_set.all %}
        <p>
            {{ forloop.counter }}
            <a href="{% url 'articles:detail' article.pk %}">{{ article.title }}</a>
        </p>
        {% endfor %}
    </div>

    <div class="col-6">
        <h3>작성한 댓글</h3>
        <p class="text-muted">{{ user.comment_set.count }}개 작성 완료</p>
        {% for comment in user.comment_set.all %}
        <p>
            {{ forloop.counter }}
            <a href="{% url 'articles:detail' comment.article.id %}">{{ comment.content }}</a>
            {% comment %} <a href="{% url 'articles:detail' comment.article.pk %}">{{ comment.content }}</a> {% endcomment %}
        </p>
        {% endfor %}
    </div>
</div>

{% endblock %}
```
<br>

64. user가 작성한 글 중 첫번쨰 글의 댓글에서 첫번쨰 user?
- `user.article_set_all()`: article로 이뤄진 QuerySet
- `user.article_set_all()[0]`: article 인스턴스
- `user.article_set_all()[0].comment_set.all()`: article 인스턴스의 댓글들(comment로 이뤄진 QuerySet)
- `user.article_set_all()[0].comment_set.all()[0]`: article 인스턴스의 댓글들 중에서 첫번째
- `user.article_set_all()[0].comment_set.all()[0].user`: article 인스턴스의 댓글들 중에서 첫번째 댓글의 유저

<br>

# 중간정리
- 참조, 역참조
```python
# articles.models.py
class Article(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = ProcessedImageField(upload_to='images/', blank=True,
                                processors=[ResizeToFill(1200, 960)],
                                format='JPEG',
                                options={'quality': 80})
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
```
- user.article.set은 존재함
- article.user.set은 존재하지 않는다: user에 정의된 것이 없다

<br>

- `request.user`
    - (로그인시) User 객체 (로그인 한 사람)
      - article.user # User 객체 (게시글 작성한 사람)
      - comment.user # User 객체 (댓글 작성한 사람)
      - User.objects.get(pk=1) # User 객체 (pk가 1인 사람)
      - User.objects.all()[0] # User 객체 (User들 중에 첫번째 있는 사람)
    - (비로그인시) AnomynousUser 객체

<br>

- `article.id` vs `article.pk`
  - id == pk

<br>

- `request.user` vs `article.user` 같은 객체?
  - 모두 User 클래스의 인스턴스는 맞음
  - A로 로그인하여 B의 게시글을 보면
  - `request.user`: A
  - `article.user`: B
  - 하지만 A로 로그인하여 A의 게시글을 보면
  - `request.user`: A
  - `article.user`: A
  - 그래서 삭제 버튼/수정 버튼을 조건문을 사용해 표시여부 나눔(둘 다 같은 User 객체이기 때문)
 
<br>

---
# N:M
65. 좋아요(LIKE)
- 좋아요(Like)
  - Article: 0명 이상의 User에게 좋아요 받음
  - User: 0개 이상의 글에 좋아요 누를 수 있음
- 로직
  - 상세보기 페이지: 좋아요 링크(`/articles/<pk>/like/`) 선택 => 좋아요 DB 추가 => redirect 상세보기 페이지
  - user 정보는 request.user에서 가져다가 사용할 예정

<br>

- model 설정(`like_users`)
```python
# articles/models.py
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from django.db import models

# Create your models here.
from django.conf import settings


class Article(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = ProcessedImageField(upload_to='images/', blank=True,
                                processors=[ResizeToFill(1200, 960)],
                                format='JPEG',
                                options={'quality': 80})
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles')


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
```
- `python manage.py makemigrations` => `python manage.py migrate`

<br>

```terminal
$ python3 manage.py shell_plus
```
- `a1 = Article.objects.all()[0]`
- `a1` => <Article: Article object (10)>
- `u1 = User.objects.all()[0]`
- `a1.like_users.add(u1)`: 좋아요 추가 코드(article 객체에 like_users.add에 user 정보)
- `a1.like_users.all()` =>  <QuerySet [<User: admin>]>
- `u1.like_articles.all()` => <QuerySet [<Article: Article object (10)>]>

<br>

- url 설정(`like`)
```python
# articles/urls.py
from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('new/', views.new, name='new'),
    path('<int:article_pk>/detail/', views.detail, name='detail'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/comments/', views.comment_create, name='comment_create'),
    path('<int:pk>/like/', views.like, name='like'),
]
```
<br>

- view 설정
```python
# articles/views.py
def like(request, pk):
    # 좋아요 추가
    
    # 상세 페이지로 redirect
    return redirect('articles:detail', pk)
```

<br>

- html 수정(`좋아요`)
```html
<!-- articles/templates/articles/detail.html -->
{% extends 'base.html' %}
{% load django_bootstrap5 %}
{% block content %}
<h2>{{ article.title }}</h2>
<p>{{ article.pk }}번</p>
<h3><a href="{% url 'accounts:detail' article.user.id %}">{{ article.user.username }}</a></h3>
<p>{{ article.created_at|date:'SHORT_DATETIME_FORMAT' }} | {{ article.updated_at|date:'y-m-d l' }}</p>

<a href="{% url 'articles:like' article.pk %}">좋아요</a>

{% if request.user == article.user %}
<p>
    <a href="{% url 'articles:update' article.pk %}">글 수정</a>
</p>
{% endif %}

<p>{{ article.content }}</p>
{% if article.image %}
    <img src="{{ article.image.url }}" alt="{{ article.image }}" width="400" height="300">
{% endif %}

<h4 class="my-3">댓글</h4>
{% if request.user.is_authenticated %}
<form action="{% url 'articles:comment_create' article.pk %}" method="POST">
    {% csrf_token %}
    {% bootstrap_form comment_form layout='inline' %}
    {% bootstrap_button button_type='submit' content='OK' %}
</form>
{% endif %}

<hr>
{% for comment in comments %}
    <p>{{ comment.user.username }} | {{ comment.content }}</p>
    <hr>
{% empty %}
    <p>댓글 없엉 ㅠㅠ</p>
{% endfor %}

<a href="{% url 'articles:index' %}">메인</a>
{% endblock %}
```
<br>

- views 수정
```python
# articles/views.py
def like(request, pk):
    article = Article.objects.get(pk=pk)
    # 좋아요 추가
    article.like_users.add(request.user)
    # `a1.like_users.add(u1)`: 좋아요 추가 코드(article 객체에 like_users.add에 user 정보)랑 같은 맥락

    # 상세 페이지로 redirect
    return redirect('articles:detail', pk)
```
- DB 값 추가됨
- 좋아요 기능은 되지만 좋아요 개수가 표현되지 않음(좋아요를 눌렀는지 안눌렀는지 모름)

<br>

- html 수정(`article.like_users.count`)
```html
<!-- articles/templates/articles/detail.html -->
{% extends 'base.html' %}
{% load django_bootstrap5 %}
{% block content %}
<h2>{{ article.title }}</h2>
<p>{{ article.pk }}번</p>
<h3><a href="{% url 'accounts:detail' article.user.id %}">{{ article.user.username }}</a></h3>
<p>{{ article.created_at|date:'SHORT_DATETIME_FORMAT' }} | {{ article.updated_at|date:'y-m-d l' }}</p>

<a href="{% url 'articles:like' article.pk %}">좋아요 | <span>{{ article.like_users.count }}</span></a>

{% if request.user == article.user %}
<p>
    <a href="{% url 'articles:update' article.pk %}">글 수정</a>
</p>
{% endif %}

<p>{{ article.content }}</p>
{% if article.image %}
    <img src="{{ article.image.url }}" alt="{{ article.image }}" width="400" height="300">
{% endif %}

<h4 class="my-3">댓글</h4>
{% if request.user.is_authenticated %}
<form action="{% url 'articles:comment_create' article.pk %}" method="POST">
    {% csrf_token %}
    {% bootstrap_form comment_form layout='inline' %}
    {% bootstrap_button button_type='submit' content='OK' %}
</form>
{% endif %}

<hr>
{% for comment in comments %}
    <p>{{ comment.user.username }} | {{ comment.content }}</p>
    <hr>
{% empty %}
    <p>댓글 없엉 ㅠㅠ</p>
{% endfor %}

<a href="{% url 'articles:index' %}">메인</a>
{% endblock %}
```

<br>

---
66. 좋아요 확인(분기, 로그인된 유저만 사용가능)
- view 수정(`if`, `remove`, `login_required`)
```python
# articles/views.py
@login_required
def like(request, pk):
    article = Article.objects.get(pk=pk)
    # 만약 로그인한 유저가 이 글을 좋아요 눌렀다면,
    if request.user in article.like_users.all():
        # 좋아요 삭제
        article.like_users.remove(request.user)

    else:
        # 좋아요 추가
        article.like_users.add(request.user)

    return redirect('articles:detail', pk)
```
- 전체 쿼리셋에서 확인하는 쿼리 메서드를 사용
- 다른 쿼리 메서드 사용할 수 있음(`filter`)
- `if article.like_users.filter(id=request.user.id).exists()`
- `id`가 `request` => `user` => `id`가 존재(`exists`)하는지
- `exists` 메서드: 모든 `article.like_users.all()`을 다 가져올 필요없음, 있는지 아닌지만 확인가능

<br>

- `get` vs `filter`
- get: 한 개 있으면 해당 객체 줌, 없으면 오류, 많아도 오류
- get 사용시기: 하나의 객체를 가져올 때 사용, get은 가지고 오더라도 그 객체
- filter: 개수에 상관없이 쿼리셋 => `exists` `get` 뒤에 사용 못함

<br>

- html 수정(`if request.user in article.like_users.all`)
- detail 화면에서 `좋아요` 선택시 좋아요 확인/취소 가능
```html
<!-- articles/templates/articles/detail.html -->
{% extends 'base.html' %}
{% load django_bootstrap5 %}
{% block content %}
<h2>{{ article.title }}</h2>
<p>{{ article.pk }}번</p>
<h3><a href="{% url 'accounts:detail' article.user.id %}">{{ article.user.username }}</a></h3>
<p>{{ article.created_at|date:'SHORT_DATETIME_FORMAT' }} | {{ article.updated_at|date:'y-m-d l' }}</p>

<a href="{% url 'articles:like' article.pk %}">
{% if request.user in article.like_users.all %}
    좋아요 취소
{% else %}
    좋아요
{% endif%}
</a> | <span>{{ article.like_users.count }}</span>

{% if request.user == article.user %}
<p>
    <a href="{% url 'articles:update' article.pk %}">글 수정</a>
</p>
{% endif %}

<p>{{ article.content }}</p>
{% if article.image %}
    <img src="{{ article.image.url }}" alt="{{ article.image }}" width="400" height="300">
{% endif %}

<h4 class="my-3">댓글</h4>
{% if request.user.is_authenticated %}
<form action="{% url 'articles:comment_create' article.pk %}" method="POST">
    {% csrf_token %}
    {% bootstrap_form comment_form layout='inline' %}
    {% bootstrap_button button_type='submit' content='OK' %}
</form>
{% endif %}

<hr>
{% for comment in comments %}
    <p>{{ comment.user.username }} | {{ comment.content }}</p>
    <hr>
{% empty %}
    <p>댓글 없엉 ㅠㅠ</p>
{% endfor %}

<a href="{% url 'articles:index' %}">메인</a>
{% endblock %}
```

<br>

---
67.  좋아요 꾸미기(icon)
- bootstrap CDN
- html 수정(`CDN`, `load static`, `<link rel="stylesheet" href="{% static 'css/style.css' %}">`: css 추가)
```html
<!-- templates/base.html -->
{% load django_bootstrap5 %}

{% load static %}

<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>

        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.2/font/bootstrap-icons.css">

        {% bootstrap_css %}
        {% block css %}{% endblock css %}

        <link rel="stylesheet" href="{% static 'css/style.css' %}">

    </head>
    <body>
        ...생략
    </body>
</html>
```
<br>

- html 수정(`좋아요 텍스트` 대신 `icon heart`, `request.user.is_authenticated`)
```html
<!-- articles/templates/articles/detail.html -->
{% extends 'base.html' %}
{% load django_bootstrap5 %}
{% block content %}
<h2>{{ article.title }}</h2>
<p>{{ article.pk }}번</p>
<h3><a href="{% url 'accounts:detail' article.user.id %}">{{ article.user.username }}</a></h3>
<p>{{ article.created_at|date:'SHORT_DATETIME_FORMAT' }} | {{ article.updated_at|date:'y-m-d l' }}</p>

{% if request.user.is_authenticated %}
    <a class="like-heart" href="{% url 'articles:like' article.pk %}">
    {% if request.user in article.like_users.all %}
        <i class="bi bi-heart-fill"></i>
    {% else %}
        <i class="bi bi-heart"></i> 
    {% endif%}</a>{{ article.like_users.count }}</span>
{% endif %}

{% if request.user == article.user %}
<p>
    <a href="{% url 'articles:update' article.pk %}">글 수정</a>
</p>
{% endif %}

<p>{{ article.content }}</p>
{% if article.image %}
    <img src="{{ article.image.url }}" alt="{{ article.image }}" width="400" height="300">
{% endif %}

<h4 class="my-3">댓글</h4>
{% if request.user.is_authenticated %}
<form action="{% url 'articles:comment_create' article.pk %}" method="POST">
    {% csrf_token %}
    {% bootstrap_form comment_form layout='inline' %}
    {% bootstrap_button button_type='submit' content='OK' %}
</form>
{% endif %}

<hr>
{% for comment in comments %}
    <p>{{ comment.user.username }} | {{ comment.content }}</p>
    <hr>
{% empty %}
    <p>댓글 없엉 ㅠㅠ</p>
{% endfor %}

<a href="{% url 'articles:index' %}">메인</a>
{% endblock %}
```

<br>

---
68. 유저가 좋아요 누른 글 확인
- html 수정
- 기존 accounts/detail 페이지
```html
<!-- accounts/templates/accounts/detail.html -->
{% extends 'base.html' %}
{% block content %}
<h1>{{ user.username }}님의 프로필</h1>
<p>{{ user.email }} | {{ user.full_name }}</p>
<div class="row">
    <div class="col-6">
        <h3>작성한 글</h3>
        <p class="text-muted">{{ user.article_set.count }}개 작성 완료</p>
        {% for article in user.article_set.all %}
        <p>
            {{ forloop.counter }}
            <a href="{% url 'articles:detail' article.pk %}">{{ article.title }}</a>
        </p>
        {% endfor %}
    </div>

    <div class="col-6">
        <h3>작성한 댓글</h3>
        <p class="text-muted">{{ user.comment_set.count }}개 작성 완료</p>
        {% for comment in user.comment_set.all %}
        <p>
            {{ forloop.counter }}
            <a href="{% url 'articles:detail' comment.article.id %}">{{ comment.content }}</a>
        </p>
        {% endfor %}
    </div>
</div>

{% endblock %}
```
<br>

- 수정 후 accounts/detail 페이지(`like_articles`)
```html
<!-- accounts/templates/accounts/detail.html -->
{% extends 'base.html' %}
{% block content %}
<h1>{{ user.username }}님의 프로필</h1>
<p>{{ user.email }} | {{ user.full_name }}</p>
<div class="row">
    <div class="col-6">
        <h3>작성한 글</h3>
        <p class="text-muted">{{ user.article_set.count }}개 작성 완료</p>
        {% for article in user.article_set.all %}
        <p>
            {{ forloop.counter }}
            <a href="{% url 'articles:detail' article.pk %}">{{ article.title }}</a>
        </p>
        {% endfor %}
    </div>

    <div class="col-6">
        <h3>좋아요 누른 글</h3>
        <p class="text-muted">{{ user.like_articles.count }}개 작성 완료</p>
        {% for article in user.like_articles.all %}
        <p>
            {{ forloop.counter }}
            <a href="{% url 'articles:detail' article.pk %}">{{ article.title }}</a>
        </p>
        {% endfor %}
    </div>
</div>

{% endblock %}
```
<br>

- 글로 들어갔을 경우 좋아요 개수 안보임(`article.like_users.count` if 문 뒤로 빼줌)
- html 수정(`article.like_users.count`)
```html
<!-- articles/templates/articles/detail.html -->
{% extends 'base.html' %}
{% load django_bootstrap5 %}
{% block content %}
<h2>{{ article.title }}</h2>
<p>{{ article.pk }}번</p>
<h3><a href="{% url 'accounts:detail' article.user.id %}">{{ article.user.username }}</a></h3>
<p>{{ article.created_at|date:'SHORT_DATETIME_FORMAT' }} | {{ article.updated_at|date:'y-m-d l' }}</p>

<span>
{% if request.user.is_authenticated %}
    <a class="like-heart" href="{% url 'articles:like' article.pk %}">
    {% if request.user in article.like_users.all %}
        <i class="bi bi-heart-fill"></i>
    {% else %}
        <i class="bi bi-heart"></i> 
    {% endif%}</a>
{% endif %}
{{ article.like_users.count }}</span>

{% if request.user == article.user %}
<p>
    <a href="{% url 'articles:update' article.pk %}">글 수정</a>
</p>
{% endif %}

<p>{{ article.content }}</p>
{% if article.image %}
    <img src="{{ article.image.url }}" alt="{{ article.image }}" width="400" height="300">
{% endif %}

<h4 class="my-3">댓글</h4>
{% if request.user.is_authenticated %}
<form action="{% url 'articles:comment_create' article.pk %}" method="POST">
    {% csrf_token %}
    {% bootstrap_form comment_form layout='inline' %}
    {% bootstrap_button button_type='submit' content='OK' %}
</form>
{% endif %}

<hr>
{% for comment in comments %}
    <p>{{ comment.user.username }} | {{ comment.content }}</p>
    <hr>
{% empty %}
    <p>댓글 없엉 ㅠㅠ</p>
{% endfor %}

<a href="{% url 'articles:index' %}">메인</a>
{% endblock %}
```

<br>

---
# 팔로우
69. 팔로우: user와 user와의 관계
- model 설정(`followings`)
```python
# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')

    @property
    def full_name(self):
        return f'{self.last_name}{self.first_name}'
```
- `python manage.py makemigrations`
- `python manage.py migrate`

<br>

- url 설정(`follow`)
```python
# accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('update/', views.update, name='update'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/follow/', views.follow, name='follow'),
]
```
<br>

- view 설정(`follow`)
```python
# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Create your views here.
def signup(request):
    ...
    return render(request, 'accounts/signup.html', context)

def detail(request, pk):
    ...
    return render(request, 'accounts/detail.html', context)

def login(request):
    ...
    return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    messages.warning(request, '로그아웃!')
    return redirect('articles:index')

@login_required
def update(request):
    ...
    return render(request, 'accounts/update.html', context)

def follow(request, pk):
    # 팔로우 상태가 아니면, '팔로우' 누르면 추가(add)
    # (이미) 팔로우 상태이면, '팔로우 취소' 버튼 누르면 삭제(remove)
    return redirect('accounts:detail', pk)
```
<br>

- html 수정(`팔로우 버튼`, `팔로우 수`)
```html
<!-- accounts/templates/accounts/detail.html -->
{% extends 'base.html' %}
{% block content %}
<h1>{{ user.username }}님의 프로필</h1>
<p>{{ user.email }} | {{ user.full_name }}</p>
<p>팔로우: {{ user.followings.count }} | 팔로워: {{ user.followers.count }}</p>
<a href="{% url 'accounts:follow' user.pk %}">팔로우</a>
<div class="row">
    <div class="col-6">
        <h3>작성한 글</h3>
        <p class="text-muted">{{ user.article_set.count }}개 작성 완료</p>
        {% for article in user.article_set.all %}
        <p>
            {{ forloop.counter }}
            <a href="{% url 'articles:detail' article.pk %}">{{ article.title }}</a>
        </p>
        {% endfor %}
    </div>

    <div class="col-6">
        <h3>좋아요 누른 글</h3>
        <p class="text-muted">{{ user.like_articles.count }}개 작성 완료</p>
        {% for article in user.like_articles.all %}
        <p>
            {{ forloop.counter }}
            <a href="{% url 'articles:detail' article.pk %}">{{ article.title }}</a>
        </p>
        {% endfor %}
    </div>
</div>

{% endblock %}
```

<br>

---
70. 팔로워 증가
- view 수정
```python
# accounts/views.py
def follow(request, pk):
    # 팔로우 상태가 아니면, '팔로우' 누르면 추가(add)
    # User: get_user_model()함수 호출하여 class 가지고 오기
    # User = get_user_model()
    # user = User.objects.get(pk=pk)
    # 2줄을 밑 한줄로 표현
    user = get_user_model().objects.get(pk=pk)
    
    # 팔로워 증가
    user.followers.add(request.user)
    # (이미) 팔로우 상태이면, '팔로우 취소' 버튼 누르면 삭제(remove)
    return redirect('accounts:detail', pk)
```
<br>

- 팔로우 생성/취소, 로그인한 유저만 팔로우 가능
- view 수정(`follow`, `login_required`)
```python
# accounts/views.py
@login_required
def follow(request, pk):
    # 프로필에 해당하는 유저를 로그인한 유저가!
    user = get_user_model().objects.get(pk=pk)
    # user에 followers의 all 전부들 중에 request.user가 있나요?
    if request.user in user.followers.all():
        # 있으면
        # (이미) 팔로우 상태이면, '팔로우 취소' 버튼 누르면 삭제(remove)
        user.followers.remove(request.user)
    else:
        # 없으면
        # 팔로우 상태가 아니면, '팔로우' 누르면 추가(add)
        user.followers.add(request.user)
    return redirect('accounts:detail', pk)
```
<br>

- html 수정(로그인 분기, 본인 팔로우버튼 if문 분기)
```html
<!-- accounts/templates/accounts/detail.html -->
{% extends 'base.html' %}
{% block content %}
<h1>{{ user.username }}님의 프로필</h1>
<p>{{ user.email }} | {{ user.full_name }}</p>
<p>팔로우: {{ user.followings.count }} | 팔로워: {{ user.followers.count }}</p>

{% if request.user != user %}
<a href="{% url 'accounts:follow' user.pk %}">
    {% if request.user in user.followers.all%}
        팔로우 취소
    {% else %}
        팔로우
    {% endif %}
</a>
{% endif %}

<div class="row">
    <div class="col-6">
        <h3>작성한 글</h3>
        <p class="text-muted">{{ user.article_set.count }}개 작성 완료</p>
        {% for article in user.article_set.all %}
        <p>
            {{ forloop.counter }}
            <a href="{% url 'articles:detail' article.pk %}">{{ article.title }}</a>
        </p>
        {% endfor %}
    </div>
    <div class="col-6">
        <h3>좋아요 누른 글</h3>
        <p class="text-muted">{{ user.like_articles.count }}개 작성 완료</p>
        {% for article in user.like_articles.all %}
        <p>
            {{ forloop.counter }}
            <a href="{% url 'articles:detail' article.pk %}">{{ article.title }}</a>
        </p>
        {% endfor %}
    </div>
</div>

{% endblock %}
```
<br>

- view 수정(본인 팔로우 불가능 if)
```python
# accounts/views.py
@login_required
def follow(request, pk):
    user = get_user_model().objects.get(pk=pk)

    if request.user == user:
        messages.warning(request, '본인 팔로우 불가능!')
        return redirect('accounts:detail', pk)

    if request.user in user.followers.all():
        user.followers.remove(request.user)
    else:
        user.followers.add(request.user)
    return redirect('accounts:detail', pk)
```

<br>

---
71. 404 error
- 404 에러(`get_object_or_404`)
- 사용자가 억지로 url로 들어갈 경우 500번대 에러 => 404 Page not found 발생하도록 만듬
- view 설정
```python
# articles/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Article
from .forms import ArticleForm, CommentForm

# Create your views here.
def index(request):
    articles = Article.objects.order_by('-pk')
    context = {
        'articles': articles
    }
    return render(request, 'articles/index.html', context)

@login_required 
def new(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
            article = article_form.save(commit=False)
            # 로그인한 유저 => 작성자임
            article.user = request.user
            article.save()
            messages.success(request, '글 작성 완료')
            return redirect('articles:index')
    else:
        article_form = ArticleForm()
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/form.html', context)

def detail(request, article_pk):
    # article = Article.objects.get(pk=article_pk)
    article= get_object_or_404(Article, pk=article_pk)
    comment_form = CommentForm()
    context = {
        'article': article,
        'comments': article.comment_set.all(),
        'comment_form': comment_form,
    }
    return render(request, 'articles/detail.html', context)


from django.contrib.auth.decorators import login_required
@ login_required
def update(request, pk):
    # article = Article.objects.get(pk=pk)
    article = get_object_or_404(Article, pk=pk)
    if request.user == article.user:
        if request.method == 'POST':
            article_form = ArticleForm(request.POST, request.FILES, instance=article)
            if article_form.is_valid():
                article_form.save()
                messages.success(request, '글 수정 완료')
                return redirect('articles:detail', article.pk)
        else:
            article_form = ArticleForm(instance=article)
        context = {
            'article_form': article_form
        }
        return render(request, 'articles/form.html', context)
    else:
        messages.warning(request, '작성자만 작성 가능!')
        return redirect('articles:detail', article.pk)

def delete(request, pk):
    # article = Article.objects.get(pk=pk)
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    return redirect('articles:index')

@login_required
def comment_create(request, pk):
    # article = Article.objects.get(pk=pk)
    article = get_object_or_404(Article, pk=pk)
    comment_form = CommentForm(request.POST)

    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article = article
        comment.user = request.user
        comment.save()
    return redirect('articles:detail', article.pk)

@login_required
def like(request, pk):
    # article = Article.objects.get(pk=pk)
    article = get_object_or_404(Article, pk=pk)
    if request.user in article.like_users.all():
        article.like_users.remove(request.user)
    else:
        article.like_users.add(request.user)

    return redirect('articles:detail', pk)
```
<br>

- view 수정
```python
# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Create your views here.
def signup(request):
    if request.method =='POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() # ModelForm의 save 메서드의 리턴값은 해당 모델의 인스턴스
            auth_login(request, user) # 로그인 함수 호출
            return redirect('articles:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)

def detail(request, pk):
    # user = get_user_model().objects.get(pk=pk)
    user = get_object_or_404(get_user_model(), pk=pk)
    context = {
        'user': user
    }

    return render(request, 'accounts/detail.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'articles:index')
        pass
    else:
        form  = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    messages.warning(request, '로그아웃!')
    return redirect('articles:index')

@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:detail', request.user.pk)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/update.html', context)

@login_required
def follow(request, pk):
    # user = get_user_model().objects.get(pk=pk)
    user = get_object_or_404(get_user_model(), pk=pk)
    if request.user == user:
        messages.warning(request, '본인 팔로우 불가능!')
        return redirect('accounts:detail', pk)
        
    if request.user in user.followers.all():
        user.followers.remove(request.user)
    else:
        user.followers.add(request.user)
    return redirect('accounts:detail', pk)
```

<br>

---
72. decorator
- view 설정(`require_POST`, `require_GET`, `require_safe`)
- redirect는 get 요청만 가능: URL 자체만 rediration 해줌, POST 요청시 보낸 데이터를 rederation 해주지 않는다(https://developer.mozilla.org/ko/docs/Web/HTTP/Redirections)
```python
# articles/views.py
# https://www.postman.com/: 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.views.decorators.http import require_POST, require_GET, require_safe

from .models import Article
from .forms import ArticleForm, CommentForm

@require_safe
def index(request):
    articles = Article.objects.order_by('-pk')
    context = {
        'articles': articles
    }
    return render(request, 'articles/index.html', context)
```

<br>

---
# 비동기 AJAX
- html 생성(CDN 가져오기)
- https://axios-http.com/kr/docs/intro
1) 어떤 이벤트일때 요청을 보낼지
    - form을 작성하면
    - /articles/<pk>/comments/
2) 서버에서 어떤 응답을 JSON으로 보내서
    - 댓글 정보를 보내서
3) DOM 조작을 어떻게 할지
    - 댓글 목록 추가

<br>

1.  좋아요 비동기
- html 수정(`like-btn`, `script`)
```html
<!-- articles/templates/articles/detail.html -->
{% extends 'base.html' %}
{% load django_bootstrap5 %}
{% block content %}
<h2>{{ article.title }}</h2>
<p>{{ article.pk }}번</p>
<h3><a href="{% url 'accounts:detail' article.user.id %}">{{ article.user.username }}</a></h3>
<p>{{ article.created_at|date:'SHORT_DATETIME_FORMAT' }} | {{ article.updated_at|date:'y-m-d l' }}</p>


<span>
{% if request.user.is_authenticated %}
    <a class="like-heart" href="{% url 'articles:like' article.pk %}">
    {% if request.user in article.like_users.all %}
        <i id="like-btn" class="bi bi-heart-fill"></i>
    {% else %}
        <i id="like-btn" class="bi bi-heart"></i> 
    {% endif%}</a>
{% endif %}

{{ article.like_users.count }}</span>
{% if request.user == article.user %}
<p>
    <a href="{% url 'articles:update' article.pk %}">글 수정</a>
</p>
{% endif %}

<p>{{ article.content }}</p>
{% if article.image %}
    <img src="{{ article.image.url }}" alt="{{ article.image }}" width="400" height="300">
{% endif %}

<h4 class="my-3">댓글</h4>
{% if request.user.is_authenticated %}
<form action="{% url 'articles:comment_create' article.pk %}" method="POST">
    {% csrf_token %}
    {% bootstrap_form comment_form layout='inline' %}
    {% bootstrap_button button_type='submit' content='OK' %}
</form>
{% endif %}

<hr>
{% for comment in comments %}
    <p>{{ comment.user.username }} | {{ comment.content }}</p>
    <hr>
{% empty %}
    <p>댓글 없엉 ㅠㅠ</p>
{% endfor %}


<script>
    // (1) 좋아요 버튼
    const likeBtn = document.querySelector('#like-btn')
    // (2) 좋아요 버튼 클릭 => 함수 실행
    likeBtn.addEventListener('click', function () {
        alert('좋아!')
    })
</script>


<a href="{% url 'articles:index' %}">메인</a>
{% endblock %}
```
- 좋아요 버튼 클릭하면 알람창 뜸

<br>

- 서버 요청보내기
- html 수정(CDN 추가, a태그 제거(console에서 깜박거리는 이유), `script`)
```html
<!-- articles/templates/articles/detail.html -->
{% extends 'base.html' %}
{% load django_bootstrap5 %}
{% block content %}
<h2>{{ article.title }}</h2>
<p>{{ article.pk }}번</p>
<h3><a href="{% url 'accounts:detail' article.user.id %}">{{ article.user.username }}</a></h3>
<p>{{ article.created_at|date:'SHORT_DATETIME_FORMAT' }} | {{ article.updated_at|date:'y-m-d l' }}</p>

<span>
{% if request.user.is_authenticated %}
    {% if request.user in article.like_users.all %}
        <i id="like-btn" data-article-id="{{ article.pk }}" class="bi bi-heart-fill"></i>
    {% else %}
        <i id="like-btn" data-article-id="{{ article.pk }}" class="bi bi-heart"></i> 
    {% endif %}
{% endif %}
{{ article.like_users.count }}</span>

{% if request.user == article.user %}
<p>
    <a href="{% url 'articles:update' article.pk %}">글 수정</a>
</p>
{% endif %}

<p>{{ article.content }}</p>
{% if article.image %}
    <img src="{{ article.image.url }}" alt="{{ article.image }}" width="400" height="300">
{% endif %}

<h4 class="my-3">댓글</h4>
{% if request.user.is_authenticated %}
<form action="{% url 'articles:comment_create' article.pk %}" method="POST">
    {% csrf_token %}
    {% bootstrap_form comment_form layout='inline' %}
    {% bootstrap_button button_type='submit' content='OK' %}
</form>
{% endif %}

<hr>
{% for comment in comments %}
    <p>{{ comment.user.username }} | {{ comment.content }}</p>
    <hr>
{% empty %}
    <p>댓글 없엉 ㅠㅠ</p>
{% endfor %}

<script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
<script>
    // (1) 좋아요 버튼
    const likeBtn = document.querySelector('#like-btn')
    // (2) 좋아요 버튼 클릭 => 함수 실행
    likeBtn.addEventListener('click', function (event) {
        // 서버로 비동기 요청하고 싶음
        console.log(event.target.dataset)
        axios({
            method: 'get',
            url: `/articles/${event.target.dataset.articleId}/like/`
        })
    })
</script>



<a href="{% url 'articles:index' %}">메인</a>
{% endblock %}
```
<br>

- html 수정(`script` 부분: `then`)
```html
<!-- articles/templates/articles/detail.html -->
<script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
<script>
    // (1) 좋아요 버튼
    const likeBtn = document.querySelector('#like-btn')
    // (2) 좋아요 버튼 클릭 => 함수 실행
    likeBtn.addEventListener('click', function (event) {
        // 서버로 비동기 요청하고 싶음
        console.log(event.target.dataset)
        axios({
            method: 'get',
            url: `/articles/${event.target.dataset.articleId}/like/`
        })
        .then(response => {
            console.log(response)
        })
    })
</script>
```
- `console`: 200과 함께 html이 옴

<br>

- views 수정(`JsonResponse` 클래스, `like` 함수 수정)
```python
# articles/views.py
from django.http import JsonResponse
@login_required
def like(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user in article.like_users.all():
        article.like_users.remove(request.user)
    else:
        article.like_users.add(request.user)

    # return redirect('articles:detail', pk)
    return JsonResponse({'hi': '안녕'})
```
- 개발자 도구(console): data에 {'hi': '안녕'}이 나옴

<br>

- view 수정(`is_liked`)
```python
from django.http import JsonResponse
@login_required
def like(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user in article.like_users.all():
        article.like_users.remove(request.user)
        is_liked = False
    else:
        article.like_users.add(request.user)
        is_liked = True
    return JsonResponse({'isLiked': is_liked})
```
<br>

- html 수정(`script` 부분)
- 방법1
```html
<!-- articles/templates/articles/detail.html -->
<script>
    const likeBtn = document.querySelector('#like-btn')
    likeBtn.addEventListener('click', function (event) {
        console.log(event.target.dataset)
        axios({
            method: 'get',
            url: `/articles/${event.target.dataset.articleId}/like/`
        })

        .then(response => {
            console.log(response)
            console.log(response.data)
            event.target.classList.toggle('bi-heart')
            event.target.classList.toggle('bi-heart-fill')
        })

    })
</script>
```
- 방법2(`script` 부분)
```html
<!-- articles/templates/articles/detail.html -->
<script>
    const likeBtn = document.querySelector('#like-btn')
    likeBtn.addEventListener('click', function (event) {
        console.log(event.target.dataset)
        axios({
            method: 'get',
            url: `/articles/${event.target.dataset.articleId}/like/`
        })

        .then(response => {
            console.log(response)
            console.log(response.data)
            // event.target.classList.toggle('bi-heart')
            // event.target.classList.toggle('bi-heart-fill')
            if (response.data.isLiked === true) {
                event.target.classList.add('bi-heart-fill')
                event.target.classList.remove('bi-heart')
            } else {
                event.target.classList.add('bi-heart')
                event.target.classList.remove('bi-heart-fill')
            }
        })

    })
</script>
```
- terminal: `"GET /articles/3/like/ HTTP/1.1" 200 18` => `"GET /articles/3/like/ HTTP/1.1" 200 17` 계속 바뀜

<br>

- heart 숫자 바꾸기
- view 수정(`context`: like 값 들, `count`값)
```python
# articles/views.py
from django.http import JsonResponse
@login_required
def like(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user in article.like_users.all():
        article.like_users.remove(request.user)
        is_liked = False
    else:
        article.like_users.add(request.user)
        is_liked = True
    context = {'isLiked': is_liked, 'likeCount': article.like_users.count() }
    return JsonResponse(context)
```

- html 수정(`<span id="like-count">{{ article.like_users.count }}</span>`, `likeCount.innerText = response.data.likeCount`)
```html
<!-- articles/templates/articles/detail.html -->
{% extends 'base.html' %}
{% load django_bootstrap5 %}
{% block content %}
<h2>{{ article.title }}</h2>
<p>{{ article.pk }}번</p>
<h3><a href="{% url 'accounts:detail' article.user.id %}">{{ article.user.username }}</a></h3>
<p>{{ article.created_at|date:'SHORT_DATETIME_FORMAT' }} | {{ article.updated_at|date:'y-m-d l' }}</p>


{% if request.user.is_authenticated %}
    {% if request.user in article.like_users.all %}
        <i id="like-btn" data-article-id="{{ article.pk }}" class="bi bi-heart-fill"></i>
    {% else %}
        <i id="like-btn" data-article-id="{{ article.pk }}" class="bi bi-heart"></i> 
    {% endif %}
{% endif %}
<span id="like-count">{{ article.like_users.count }}</span>

{% if request.user == article.user %}
<p>
    <a href="{% url 'articles:update' article.pk %}">글 수정</a>
</p>
{% endif %}

<p>{{ article.content }}</p>
{% if article.image %}
    <img src="{{ article.image.url }}" alt="{{ article.image }}" width="400" height="300">
{% endif %}

<h4 class="my-3">댓글</h4>
{% if request.user.is_authenticated %}
<form action="{% url 'articles:comment_create' article.pk %}" method="POST">
    {% csrf_token %}
    {% bootstrap_form comment_form layout='inline' %}
    {% bootstrap_button button_type='submit' content='OK' %}
</form>
{% endif %}

<hr>
{% for comment in comments %}
    <p>{{ comment.user.username }} | {{ comment.content }}</p>
    <hr>
{% empty %}
    <p>댓글 없엉 ㅠㅠ</p>
{% endfor %}

<script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
<script>
    const likeBtn = document.querySelector('#like-btn')
    likeBtn.addEventListener('click', function (event) {
        console.log(event.target.dataset)
        axios({
            method: 'get',
            url: `/articles/${event.target.dataset.articleId}/like/`
        })
        .then(response => {
            console.log(response)
            console.log(response.data)
            if (response.data.isLiked === true) {
                event.target.classList.add('bi-heart-fill')
                event.target.classList.remove('bi-heart')
            } else {
                event.target.classList.add('bi-heart')
                event.target.classList.remove('bi-heart-fill')
            }
            const likeCount = document.querySelector('#like-count')
            likeCount.innerText = response.data.likeCount
        })
    })
</script>

<a href="{% url 'articles:index' %}">메인</a>
{% endblock %}
```

<br>

---
74. 댓글 비동기
- html 수정(`id="comment-form"`, `script`생성 )
```html
<!-- articles/templates/articles/detail.html -->
{% extends 'base.html' %}
{% load django_bootstrap5 %}
{% block content %}
<h2>{{ article.title }}</h2>
<p>{{ article.pk }}번</p>
<h3><a href="{% url 'accounts:detail' article.user.id %}">{{ article.user.username }}</a></h3>
<p>{{ article.created_at|date:'SHORT_DATETIME_FORMAT' }} | {{ article.updated_at|date:'y-m-d l' }}</p>


{% if request.user.is_authenticated %}
    {% if request.user in article.like_users.all %}
        <i id="like-btn" data-article-id="{{ article.pk }}" class="bi bi-heart-fill"></i>
    {% else %}
        <i id="like-btn" data-article-id="{{ article.pk }}" class="bi bi-heart"></i> 
    {% endif %}
{% endif %}
<span id="like-count">{{ article.like_users.count }}</span>

{% if request.user == article.user %}
<p>
    <a href="{% url 'articles:update' article.pk %}">글 수정</a>
</p>
{% endif %}

<p>{{ article.content }}</p>
{% if article.image %}
    <img src="{{ article.image.url }}" alt="{{ article.image }}" width="400" height="300">
{% endif %}

<h4 class="my-3">댓글</h4>
{% if request.user.is_authenticated %}
<form id="comment-form" action="{% url 'articles:comment_create' article.pk %}" method="POST">
    {% csrf_token %}
    {% bootstrap_form comment_form layout='inline' %}
    {% bootstrap_button button_type='submit' content='OK' %}
</form>
{% endif %}

<hr>
{% for comment in comments %}
    <p>{{ comment.user.username }} | {{ comment.content }}</p>
    <hr>
{% empty %}
    <p>댓글 없엉 ㅠㅠ</p>
{% endfor %}

<script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
<script>
    const likeBtn = document.querySelector('#like-btn')
    likeBtn.addEventListener('click', function (event) {
        console.log(event.target.dataset)
        axios({
            method: 'get',
            url: `/articles/${event.target.dataset.articleId}/like/`
        })
        .then(response => {
            console.log(response)
            console.log(response.data)
            // event.target.classList.toggle('bi-heart')
            // event.target.classList.toggle('bi-heart-fill')
            if (response.data.isLiked === true) {
                event.target.classList.add('bi-heart-fill')
                event.target.classList.remove('bi-heart')
            } else {
                event.target.classList.add('bi-heart')
                event.target.classList.remove('bi-heart-fill')
            }
            const likeCount = document.querySelector('#like-count')
            likeCount.innerText = response.data.likeCount
        })
    })
</script>

<script>
    // 댓글
    // (1) 댓글 폼
    const commentForm = document.querySelector('#comment-form')
    // (2) 제출하면, 함수 실행시킴
    commentForm.addEventListener('submit', function() {
        console.log('hi')

    })
</script>
<a href="{% url 'articles:index' %}">메인</a>
{% endblock %}
```
- console: 댓글 입력시 `hi` 나타남(잠깐 나타났다가 사라짐)

<br>

- html 수정(`script`, `event.preventDefault();`)
```html
<!-- articles/templates/articles/detail.html -->
<script>
    // 댓글
    // (1) 댓글 폼
    const commentForm = document.querySelector('#comment-form')
    // (2) 제출하면, 함수 실행시킴
    commentForm.addEventListener('submit', function(event) {
        event.preventDefault();
        console.log('hi')

    })
</script>
```
- console: 댓글을 입력하면 `hi` 사라지지않고 그래로 표시됨

<br>

- html 수정(데이터 보내기, `action="{% url 'articles:comment_create' article.pk %}" method="POST"` 삭제, `script` 수정)
```html
<!-- articles/templates/articles/detail.html -->
...

<h4 class="my-3">댓글</h4>
{% if request.user.is_authenticated %}

{% comment %} <form id="comment-form" action="{% url 'articles:comment_create' article.pk %}" method="POST"> {% endcomment %}
<form id="comment-form" data-article-id="{{ article.pk }}">

    {% csrf_token %}
    {% bootstrap_form comment_form layout='inline' %}
    {% bootstrap_button button_type='submit' content='OK' %}
</form>
{% endif %}

...

<script>
    // 댓글
    // (1) 댓글 폼
    const commentForm = document.querySelector('#comment-form')
    // (2) 제출하면, 함수 실행시킴
    commentForm.addEventListener('submit', function(event) {
        event.preventDefault();
        axios({
            method: 'post',
            url: `/articles/${event.target.dataset.articleId}/comments/`
        })

    })
</script>
<a href="{% url 'articles:index' %}">메인</a>
{% endblock %}
```
- console: 서버에 오류표시됨(`CSRF token missing or incorrect.`)

<br>

- csrf 토큰 보내기
- https://docs.djangoproject.com/en/4.1/howto/csrf/
- html 수정(script: `csrftoken`)
```html
<!-- articles/templates/articles/detail.html -->
<script>
    const commentForm = document.querySelector('#comment-form')

    // csrf
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    commentForm.addEventListener('submit', function(event) {
        event.preventDefault();
        axios({
            method: 'post',
            url: `/articles/${event.target.dataset.articleId}/comments/`,
            headers: {'X-CSRFToken': csrftoken},
        })
    })
</script>
```
- 댓글 작성이 안됨: 서버로 보냈지만, DB에 저장이 안되어 있기 떄문(데이터를 준적이 없기 때문)

<br>

- 서버에 데이터 넘겨주기
- html 수정(`then`)
```html
<!-- articles/templates/articles/detail.html -->
<script>
    const commentForm = document.querySelector('#comment-form')

    // csrf
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
    commentForm.addEventListener('submit', function(event) {
        event.preventDefault();
        axios({
            method: 'post',
            url: `/articles/${event.target.dataset.articleId}/comments/`,
            headers: {'X-CSRFToken': csrftoken},
            // data 넘겨주는 방법 공식처럼 외우기
            data: new FormData(commentForm)
        })
        .then(response => {
            console.log(response.data)
        })
    })
</script>
```
<br>

