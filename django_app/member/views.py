from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.http import HttpResponse
from django.shortcuts import redirect, render


app_name = 'member'

def login(request):
    """
    POST 요청이 올 경우 로그인 완료 후 post_list 뷰 이동
    실패할 경우 HttpResponse로 'Login invalid' 표시
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            django_login(request, user)
            return redirect('post:post_list')
        else:
            return HttpResponse('로그인 실패')

    else:
        if request.user.is_authenticated:
            return redirect('post:post_list')
        return render(request, 'member/login.html')


def logout(request):
    """
    로그아웃 후 post_list 뷰 이동
    """
    django_logout(request)
    return redirect('post:post_list')