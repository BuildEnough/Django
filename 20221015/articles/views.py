from django.shortcuts import render

# Create your views here.


def index(request):
    # 요청한 정보 받음

    return render(request, "articles/index.html")
    # 원하는 페이지 render
