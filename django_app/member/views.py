from django.contrib.auth import authenticate, login as auth_login
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
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print('로그인 유저', user)

        if user is not None:
            auth_login(request, user)
            return redirect('post:post_list')
        else:
            return HttpResponse('로그인 실패')

    else:
        return render(request, 'member/login.html')

