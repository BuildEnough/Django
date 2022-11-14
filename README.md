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