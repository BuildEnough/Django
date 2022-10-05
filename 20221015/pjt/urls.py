"""pjt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# include 기능을 사용하기 위해 추가

urlpatterns = [
    path("admin/", admin.site.urls),
    path("articles", include("articles.urls")),
    # 프로젝트 전체의 urls.py 파일에서 articles(앱)을 include
    # include: articles에 있는 urls 파일을 가지고 오라는 의미
    # 즉, 앱의 분리(공간적 분리)
    # path("")에서 "" 안에 들어가는 것이 url 주소 입력했을 때
    # localhost:8000/[여기에 들어감]
]

# urlpatterns 목록: URL을 views로 routing(네트워크에서 특정 경로로 데이터를 보낼때 사용되는 과정) 함
