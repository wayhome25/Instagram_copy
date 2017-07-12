from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse

from .forms import PostForm
from .models import Post

User = get_user_model()

def post_list(request):
    """
    모든 Post 목록을 'posts' 라는 key로 context에 담아서 return render 처리
    post/post_list.html을 template으로 사용한다
    각 포스트에 대해 최대 4개까지의 댓글을 보여주도록 템플릿에 설정
    """
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'post/post_list.html', context)


def post_detail(request, post_pk):
    """
    Model에서 post_pk에 해당헤는 Post 객체 리턴, 보여줌
    Model Manager의 get메서드를 사용하여 하나의 객체만 가져옴
    django.template.loader.get_template +
    django.http.HttpResponse 함수를 축약한 shortcut = render 함
    """
    try:
        post = Post.objects.get(pk=post_pk)
    except Post.DoesNotExist as e:
        # 1. 404를 띄운다
        # return HttpResponseNotFound('Post가 없어용 detail:{}'.format(e))

        # 2. post_list view로 돌아간다 - redirect 사용
        # return redirect('post:post_list')

        # 3. HttpResponseRedirect 사용
        url = reverse('post:post_list')
        return HttpResponseRedirect(url)

    template = loader.get_template('post/post_detail.html')
    context = {
        'post': post,
    }
    rendered_stirng = template.render(context=context, request=request)
    return HttpResponse(rendered_stirng)
    # render() 를 사용하면 한번에 해결가능!
    # return render('post/post_detail.html', {'post': post})



@login_required
def post_create(request):
    """
    POST 요청을 받아 Post 객체를 생성 후 post_list 페이지로 redirect
    """
    # if request.method == 'POST':
        # 제출된 form 내용으로 새로운 Post 객체 생성 후 post_detail 뷰로 redirect
        # get_user_model을 이용해서 얻은 User클래스(Django에서 인증에 사용하는 유저모델)에서 임의의 유저 한명을 가져온다.
    #     user = User.objects.first()
    #     post = Post.objects.create(
    #         author = user,
    #         photo = request.FILES['file'],
    #     )
    #     comment_string = request.POST.get('comment', '')
    #
    #     if comment_string:
    #         post.comment_set.create(
    #             author = user,
    #             content = comment_string,
    #         )
    #     return redirect('post:post_detail', post_pk=post.pk)
    # else:
    #     return render(request, 'post/post_create.html')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # ModelForm의 save 메스드를 활용해서 Post를 가져옴
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post:post_detail', post_pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'post/post_create.html', {'form': form})

def post_modify(request, post_pk):
    pass


def post_delete(request, post_pk):
    """
    post_pk에 해당하는 Post에 대한 delete 처리 후, post_list 페이지로 redirect
    """
    pass


def comment_create(request, post_pk):
    """
    POST 요청을 받아 Comment 객체 생성 후 post_list 페이지로 redirect
    """
    pass


def comment_modify(request, post_pk):
    pass


def comment_delete(request, post_pk, comment_pk):
    """
    POST 요청을 받아 Comment 객체를 delete 처리 후, post_detail 페이지로 redirect
    """


def post_anyway(request):
    return redirect('post:post_list')

