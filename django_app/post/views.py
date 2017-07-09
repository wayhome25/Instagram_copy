from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .models import Post


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'post/post_list.html', context)


def post_detail(request, post_pk):
    """
    post_pk에 해당헤는 Post 객체 리턴, 보여줌
    django.template.loader.get_template +
    django.http.HttpResponse 함수를 축약한 shortcut = render 함수
    """
    post = Post.objects.get(pk=post_pk)
    template = loader.get_template('post/post_detail.html')
    context = {
        'post': post,
    }
    rendered_stirng = template.render(context=context, request=request)
    return HttpResponse(rendered_stirng)



def post_create(request):
    """
    POST 요청을 받아 Post 객체를 생성 후 post_list 페이지로 redirect
    """


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