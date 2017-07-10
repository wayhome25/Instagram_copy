from django.contrib.auth import \
    authenticate, \
    login as django_login, \
    logout as django_logout, get_user_model
from django.http import HttpResponse
from django.shortcuts import redirect, render


User = get_user_model()

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


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if User.objects.filter(username=username).exists():
            return HttpResponse('이미 존재하는 username 입니다')
        elif password1 != password2:
            return HttpResponse('비밀번호가 일치하지 않습니다')
        user = User.objects.create_user(username=username, password=password1)
        django_login(request, user)
        return redirect('post:post_list')
    else:
        return render(request, 'member/signup.html')