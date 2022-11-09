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
29. 회원가입, 로그인
