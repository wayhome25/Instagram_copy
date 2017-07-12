from django.contrib.auth import \
    login as django_login, \
    logout as django_logout, get_user_model
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import LoginForm, SignupForm

User = get_user_model()


def login(request):
    """
    POST 요청이 올 경우 로그인 완료 후 post_list 뷰
    실패할 경우 HttpResponse로 'Login invalid' 표시
    """
    if request.method == 'POST':
        ### Form 클래스 미사용시
        # username = request.POST.get('username')
        # password = request.POST['password']
        # user = authenticate(request, username=username, password=password)
        #
        # if user is not None:
        #     django_login(request, user)
        #     return redirect('post:post_list')
        # else:
        #     return HttpResponse('로그인 실패')

        ### Form 클래스 사용시
        # Bound form 생성
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            django_login(request, user)
            return redirect('post:post_list')
        else:
            return HttpResponse('로그인 정보에 문제가 있어요!')
    else:
        if request.user.is_authenticated:
            return redirect('post:post_list')
        form = LoginForm()
        return render(request, 'member/login.html', {'form': form})


def logout(request):
    """
    로그아웃 후 post_list 뷰 이동
    """
    django_logout(request)
    return redirect('post:post_list')


def signup(request):
    """
    url : /member/signup/
    template : member/signup.html
    username, password1, password2를 받아 회원가입
    이미 유저가 있는지 검사, password1, password2 일치여부 검사
    오류 발생시 오류메시지 리턴
    성공시 로그인 시키고 post_list 리다이렉트
    """
    if request.method == 'POST':
        ### Form을 사용하지 않는 경우
        # username = request.POST['username']
        # password1 = request.POST['password1']
        # password2 = request.POST['password2']
        # if User.objects.filter(username=username).exists():
        #     return HttpResponse('이미 존재하는 username 입니다')
        # elif password1 != password2:
        #     return HttpResponse('비밀번호가 일치하지 않습니다')
        # user = User.objects.create_user(username=username, password=password1)

        ### Form을 사용한 경우
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.create_user()
            django_login(request, user)
            return redirect('post:post_list')
    else :
        form = SignupForm()
    return render(request, 'member/signup.html', {'form': form})