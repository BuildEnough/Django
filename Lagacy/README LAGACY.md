1. python -m venv [가상환경이름]
   - python -m venv venv
   - **가상환경 만들기**

<br>

---
2. source [가상환경이름]/Scripts/activate
   - Window: source venv/Scripts/activate
   - Mac: source venv/bin/activate
   - . venv/Scripts/activate
   - `.`을 사용할 경우 현재 폴더 내에서 실행한다는 의미
   - 만약 `cd venv`, 즉 venv 안에서 실행할 경우의 코드는
   - . /Scripts/activate
   - 가상환경을 실행하면 `cd`를 사용해서 이동해도 계속 가상환경이 실행됨
   - 가상환경을 실행하는 이유: 프로젝트 기초 전부를 Python/Django와 분리해줌
     - 웹사이트가 변경되어도 개발 중인 것에 영향을 미치지 않는다(독립적임)
   - **가상환경 실행**

<br>

---
3. deactivate
   - 가상환경이 계속 실행 중이기 때문에 아무런 폴더에서 `deactivate`하면 가상환경 종료됨
   - **가상환경 종료**

<br>

---
4. pip list
   - pip: 파이썬으로 작성된 패키지 라이브러리를 관리해주는 시스템
   - 가상환경을 처음 실행한 상태에서 `pip list`를 실행할 경우 아무것도 안나오는게 정상
   - **현재 내 컴퓨터에 설치된 파이썬 패키지 목록을 볼 수 있음**

<br>

---
5. pip install django==[버전]
   - pip install django==3.2.13
   - `==`를 사용하지 않고 `pip install django`하면 django의 최신버전 설치됨
   - **django 설치**

<br>

---
6. pip list
   - django 패키지가 정상적으로 설치되었는지 확인

<br>

---
7. pip freeze > requirements.txt
   - pip freeze: 현재 작업 환경(가상환경)에 설치되어 있는 패키지의 리스트를 모두 출력해줌
   - `requirements.txt` 이름을 바꿔도 상관 없지만 보통 `requirements.txt`로 함
   - **requirements.txt에 설치된 패키지들이 정렬됨**

<br>

---
8. pip install -r requirements.txt
   - `r`: read라는 의미
   - **설정파일 `requirements.txt`에 작성된 내용에 따라 패키지가 일괄 설치됨**

<br>

---
9. django-admin startproject [프로젝트_이름] [프로젝트_시작경로]
   - django-admin startproject pjt .
   - `.`에 따라 `manage.py` 파일의 생성 여부 나뉨
   - `.`: 현재 디렉토리
   - `manage.py` 위치는 상관 없지만 통일해주는 것이 좋음(연습할 땐 둘 다 해보자)
   - 앱을 실행 할 때 `manage.py`가 있는 폴더에서 명령어를 입력해줘야 하기 때문  
   - `django-admin`: `django-manage.py`는 `django-admin.py` 로 프로젝트를 생성할 떄 만들어짐
   - 처음엔 `django-admin.py`를 사용 가능하고 `django-manage.py`는 사용할 수 없다
   - [adim과_manage](https://devlog.jwgo.kr/2018/02/07/what-is-the-diff-btw-manage-django-admin/)
   - [더 자세한 정보](https://docs.djangoproject.com/ko/4.1/ref/django-admin/)
   - **`manage.py` 파일 생성**

<br>

---
10. python manage.py runserver
![서버 확인](image/python%20manage.py%20runserver.png)
      - url에 `localhost:8000` 입력
      - 정상적으로 앞의 내용을 실행했다면 표시된 화면이 나옴
      - `manage.py`: django 명령어를 인식하기 위한 중간역할, django의 명령어 인터페이스(궁금하면 직접 `manage.py` 열어보기)
      - 서버 실행 후 항상 `터미널` 에서 로그 확인
      - 포트 변경: `python manage.py runserver [원하는 포트 번호]`
      - 포트 변경: `python manage.py runserver 8080`
      - 종료: `ctrl + c`
      - **서버 구동**

<br>

---
11. [프로젝트] 안의 `settings.py` 세팅
  ```python
  LANGUAGE_CODE = 'ko-kr'

  TIME_ZONE = 'Asia/Seoul'
  ```
  - `python manage.py runserver`를 실행했을 경우 한국시간과 한국어로 변경됨

<br>

---
12.  python manage.py startapp [생성할_app_이름]
   - `python manage.py startapp articles`
   - **앱 생성**

<br>

---
13. 프로젝트 settings.py 설정


  ![INSTALLED_APPS](image/INSTALLED_APPS.png)
  - `,` 꼭 붙이기
  - **앱 등록**

<br>

---
14.  프로젝트 urls.py
   ![project_urls](image/project_urls.png)
    ```python
    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path("admin/", admin.site.urls),
        path("articles", include(articles.urls)),
    ]
    ```
    - include를 활용: 공간적 분리

<br>

---
15.  순서
  - 1번 urls.py(url 등록)
  - 2번 views.py(함수 생성)
  - 3번 templates(template 생성)

<br>

---
16. 생성한 앱 urls.py 생성(등록)
    - urlpatterns 추가
    ![앱urls](image/앱urls.jpg)
    - `views.index`가 [동그라미 1번]으로 가고, 이것을 index라는 이름으로 부름
    - `""` [동그라미 1번] 주소로 요청하면 views에 있는 index함수로 응답
    - url 대신 이름을 index로 지정
    ![앱urls_주석](image/앱urls_주석.png)
    - app_name: url namespace(url을 이름으로 분류하는 기능, url을 앱별로 분류하는 기능)
    - app_name이 없으면: 다른 앱에서 `index`라는 이름을 사용하지 못함(동일한 이름은 장고 프로젝트에서 1개만 사용할 수 있기 때문)
    - 예를 들면
      ```python
      path('', views.index, name='index')
      path('', views.index, name='index2')
      path('', views.index, name='index3')
      ```

<br>

---
17.   생성한 앱 view.py 함수 정의
  ![앱views](image/앱views.png)
    ```python
    from django.shortcuts import render

    def index(request):
        return render(request, "articles/index.html")
    ```

<br>

---
18.  Template 생성
    - 20221015(전체 폴더) => articles(앱) => templates(폴더 생성) => articles(폴더 생성) => index.html(파일 생성)
    - `python manage.py runserver` 실행
    - `localhost:8000/articles` 검색 후 실행되는지 확인
    - 실행 안될 경우
      - 프로젝트 폴더, 앱 폴더에서 `""` 혹은 오타 살펴보기

<br>

---

18.-1 templates 활용
   - 프로젝트 `settings.py`에 `TEMPLATES`에서
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
   - `'DIRS': [BASE_DIR / 'templates'],` 수정
   - 프로젝트와 동일한 경로에 `templates` 만듬
   - 생성한 앱의 `views.py`에서 경로에 따라 `base.html` 만들어줌

<br>

---

18.-2 base.html
   - `base.html`에 넣어줌
   ```html
      {% block content %}
      {% endblock %}
   ```
   - `base.html`을 사용하는 html은 `{% extends 'base.html' %}`사용해야 함
   ```html
      {% extends 'base.html' %}
      {% block content %}
      index
      {% endblock %}
   ```

<br>

---
19.  점검  
    ![URL요청](image/점검1.png)
    <br>
    - URL 요청
    <br>
    <br>
    ![서버 요청](image/점검2.png)
    - 서버로 요청
    <br>
    <br>
    ![앱 urls.py](image/점검3.jpg)
    <br>
    - 생성한 앱 폴더의 urls.py안의
    - urlpatterns의 목록 안에서
    - views.py에 있는 index함수 실행
    <br>
    <br>
    ![앱 views.py](image/점검4.jpg)
    <br>
    - 생성한 앱 폴더의 views.py안의
    - html 파일을 불러옴

<br>

---
# CRUD
20.  모델 정의
  - 1번: 클래스 정의
  - 2번: migrations 파일 생성
  - 3번: DB반영(migrate)

<br>

---
21. 요구사항에 따른 모델 작성
   - 예시
   ![요구사항](image/요구사항.png)

<br>

---
22.  생성한 앱의 models.py 클래스 정의
   ```python
   from django.db import models

   class Articles(models.Model):
      title = models.CharField(max_length=20)
      content = models.TextField()
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
   ```
   ![클래스](image/클래스.jpg)
   - Article(1번)은 Models(2번)에 있는 Model(3번)을 상속받아서 모델 만듬
   ![클래스2](image/클래스2.png)

<br>

---
23. makemigrations 파일 생성
   - python manage.py makemigrations
   ![마이그레이션 경로](image/마이그레이션_경로.png)
   - 경로를 따라가보면
   ![마이그레이션](image/마이그레이션.png)
   - `0001_initial.py` 라는 파일이 생성됨
   - db.sqlite3의 새로운 테이블을 만들기 위한 설계도
   - `migrate` 하기 전까지 아무런 내용 없음

<br>

---
24. migrate
   - python manage.py migrate
   ![마이그레이트](image/마이그레이트.jpg)
   - 1번: 앱 이름
   - 2번: 모델 이름

<br>

---
25. DB 확인
   - python manage.py showmigrations
   - DB가 제대로 생성되었는지 확인할 수 있다

<br>

---
# CRUD 구현
26. CREATE 생성
   - 기능을 만들때: URL에 mapping 되는 VIEW 함수는 각각 1개씩 필요함(특정 URL의 기능들이 다르기 때문)
   - 기능 추가
     - URL 생성 => VIEW 함수
     - URL에 대응되는 VIEW 함수를 새롭게 생성
   - `templates`에 `create.html`만들어야 함

<br>

---
27. form 태그
   - 사용자에게 정보를 입력받을 때 form 태그 사용
   - `html` 파일에서 사용
   ```html
   <body>
   <form action="% url 'article:create' %">
   </form>
   </body>
   ```
   - `create`라는 name을 가진 주소를 요청(`create`라는 path를 만들어줘야함)
   - `<form action="% url 'article:create' %">`에서
   - article은 app_name 지정해 둔 것

<br>

---
28. URL(path 만들기)
   ```python
   urlpatterns = [
      path('index/', views.index, name='practice'),
      path('new/', views.new, name='new'),
      path('create/', views.create, name='create'),
   ]
   ```
   - 생성한 앱의 `urls.py`에서 path를 만들어 줌
   ![create_path](image/create_path.jpg)
   - 1번: 주소를 create로 요청
   - 2번: views는 create 함수 요청 
   - 3번: name은 create
   - 아직 create 함수를 만들지 않았기 때문에 오류 발생

<br>

---
1.  view(함수 작성)
   ```python
   def create(request):
      return render(request, "article/index.html")
   ```

<br>

---
30. form 데이터 생성
   - html 파일 form 에서 views.py에 있는 함수로 데이터를 넘겨줘야 함
   - 함수안에 `content` 생성
   - templates에서 데이터를 get해야 됨
     - `request.GET.get()` 사용
   - html 파일의 input 태그의 name 속성에 값 지정(데이터의 이름을 지정)
   - html 예시
   ![create_html](image/create_html.jpg)
   - views 예시
   ![create_views](image/create_views.jpg)

<br>

---
31. 입력 되었는지 확인
   - view.py에 print문 추가
   - html 페이지
   ![html_print문](image/html_print.png)
   - views.py
   ![view_print문](image/views_print.png)
   - terminal
   ![terminal_print문](image/terminal_print.png)
   - 즉, **입력한 문장을 content가 정확히 받았다는 의미**

<br>

---
32. models를 받아옴
   - 생성한 앱의 모델의 데이터 생성
   - model을 import
   ![모델앱import](image/create_model_import.jpg)
   ![모델앱import2](image/create_model_import2.jpg)

<br>

---
33. DB 저장
   - 생성한 앱의 views.py
   ![DB저장](image/DB생성.jpg)
   - 1번: 클래스
   - 2번: objects에
   - 3번: create 메소드 사용
   - 4번: 필드(속성)
   - 5번: 값

<br>

---
34. 저장 확인
   ![DB저장_html](image/DB저장_html.png)
   ![DB저장_sqlite3](image/DB저장_sqlite3.png)
   ![DB저장_sql](image/DB저장_sql.png)
   
<br>

---
35. 데이터 불러오기
   - [클래스].objects.all(): 데이터 불러오는 ORM 코드
   ![DB불러오기](image/DB불러오기.jpg)
   
<br>

---
36. 변수 할당
   - 불러온 데이터를 변수에 할당
   - articles라는 변수에 할당
   ![DB변수할당](image/DB변수할당.jpg)
   
<br>

---
37. 변수 출력
   - 딕셔너리 만든 후 변수 출력
   - 딕셔너리(context)
   ![DB딕셔너리변수](image/DB딕셔너리변수.jpg)
   
<br>

---
38. 인자 넘기기
   ![DB인자넘기기](image/DB인자넘기기.jpg)
   - 함수에 인자를 넘김
   - templates 변수에서 2번을 출력하기 위해 1번을 넘겨줌
   - render라는 함수에 context 인자 넘김(templates 파일에서 변수들을 사용하기 위함)

<br>

---
39. 변수확인
   - 앱의 html 코드
   ![변수확인](image/변수확인.png)
   ![변수확인html](image/변수확인html.png)
   - 이름: QuerySet
   - 대괄호[]로 닫혀있기 때문에 리스트를 의미함
   - 리스트는 반복해서 출력해야함

<br>

---
40. DTL for문 사용
   - DTL(Django Template Language)
   ![DTL_for문](image/DTL_for문.png)
   - 변수(articles)을 article로 반복
   - {% endfor %}를 사용하여 반복문 종료
   - {{ article }}을 사용하여 나타날 항목 추가
   ![DTL_크롬](image/DTL_크롬.png)
   - 표시되지만 원하는 데이터 값이 아님

<br>

---
41. 원하는 데이터 표시
   - 생성한 앱의 models.py의 설계도를 참고하여 만들 수 있음
   ![앱models](image/앱models.png)
   
<br>

   ![원하는데이터불러오기](image/데이터불러오기html.png)
   ![크롬화면](image/원하는데이터불러오기_크롬.png)
   - article뒤에 .[원하는클래스의 지정된 변수값]을 사용하여 불러올 수 있음

<br>

---
42. 이상한 점
   ![이상한점](image/이상한점.png)
   - index와 create 함수 모두 `index.html`을 응답으로 templates를 제공함
   - create는 데이터를 만들지만 출력 안됨
   - 이유는 index함수에 있는 `context` 변수가 create함수에 없기 때문

<br>

---
43. 이상한 점 해결(정답 아님)
   ![context추가](image/이상함_context추가.jpg)
   - create에도 context 함수를 추가
   ![해결한 크롬창](image/이상한점_해결.png)
   - **하지만 context를 추가하는 것이 정답 아님**

<br>

---
44. 이상한 점 해결(redirect)
   ![redirect사용](image/redirect.png)
   - `render`대신 `redirect` 사용
   - article에 index 요청
   - create 주소가 아닌 index로 돌아오게됨

<br>

---
## delete
45. a태그 추가
   ![a태그 추가](image/delete_a태그.jpg)
   - 삭제 버튼 만들어 줌

<br>

---
46. url 만들기
   ![url](image/delete_url.jpg)
   - delete 할때 pk값이 필요함
   - pk 전달방법: `article:pk`
   - 각각의 pk 값이 동적인자(url 변수 사용 하듯이 사용)로 전달됨

<br>

---
47. delete path 만들기
   ![path 만들기](image/delete_path.png)
   - 동적인자 사용: `<int:article_pk>`
     - article_pk라는 인자(함수에서 만듬)
   - int타입 생략 가능하지만, 타입 지정해도됨

<br>

---
48. delete 함수 만들기
   ![delete_함수](image/delete_함수.jpg)
   - `views.py`에서 함수 만들기(view에 대한 함수 만들기)
   - 1번: article_pk라는 인자 받음
   - 2번: article_는 삭제할 값을 불러와 저장하는 변수
   - `article_.delete()`: (적인자로 인해 전달받은 값을 불러와서 delete함
   - 삭제 전
   ![삭제전](image/delete_삭제전.png)

<br>

   - 삭제 후
   ![삭제후](image/delete_삭제후.png)

<br>

---
# UPDATE
49. a태그 만들기
   - html의 body 안에 a태그를 만들어줌
   - 더미페이지 만들기
     - edit라는 더미페이지

<br>

   - templates에 수정을 원하는 html 파일에 a 태그 만들기
   ```html
   <a href="{% url 'edit' %}">

   </a>
   ```
   
<br>
  
50. path 만들기
   - 생성한 앱의 `urls.py`에서 path 만들기
   ![update_url](image/update_url.jpg)
   - path를 만들어 줬으므로 생성한 앱의 `views.py`에서 함수를 정의해줘야 함

<br>

---
51. 함수 만들기
   ```python
   def edit(request)
    return render(request, "artilce/edit.html")
   ```
   - 생성한 앱의 `views.py` 에서 함수 만들기
   - 다음으로 templates안의 article에 `edit.html`이 없으므로
   - `edit.html ` 만들어주기

<br>

---
52. html파일 만들기(update)
   - update html 만들때 create html을 가져옴(글 수정과 글 생성 양식이 비슷하기 때문)
   - update 는 read + create
   - read: 수정페이지에 데이터 출력

<br>

---

# URL 명시
```html
{% url [특정 path] %}
```
- URL을 명시할 때 `%`로 열고 `{}`로 닫아줌
- `특정 path`는 생성한 앱의 `urls.py`에서 설정해줌

<br>

---

<br>

---

