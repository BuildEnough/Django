from django.urls import path

# 위의 모듈 이름이 기억 안나는 경우 프로젝트의 urls.py에서 복사 후 include만 삭제

from . import views

# views 사용하기 위해 추가

# url namespace
# url을 이름으로 분류
app_name = "articles"
# app_name: 만약  index를 다른 곳에서 사용하고 싶어도 사용할 수 없기 때문
# 동일한 이름은 장고 프로젝트 내에서 1개만 사용할 수 있다

urlpatterns = [
    path("", views.index, name="index"),
    # path추가: (url = ""), (views 함수: index로 향함)
    # "" 주소로 요청: views에 있는 index를 함수로 응답
    # ''urls 대신 이름을 지정: 변수이름 지정하듯 name를 index로 지정
]
