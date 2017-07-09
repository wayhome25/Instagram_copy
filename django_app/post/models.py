"""
member application생성
    User모델 구현
        username, nickname
이후 해당 User모델을 Post나 Comment에서 author나 user항목으로 참조
"""
from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    # Django가 제공하는 기본 User와 연결되도록 수정
    author = models.ForeignKey(User)
    photo = models.ImageField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(
        User,
        related_name='like_posts',
        through='PostLike',
    )
    tags = models.ManyToManyField('Tag')

    def add_comment(self, user, content):
        """
        :param user: comment의 author 로 사용
        :param content: comment의 content로 사용
        :return: 자신을 post로 갖는 comment 객체 생성
        """
        return self.comment_set.create(author=user, content=content)

    def add_tag(self, tag_name):
        """
        tags에서 tag_name 을 name으로 갖는 Tag 객체를 가져오고, 없으면 생성하여 자신의 tags에 추가
        :param tag_name: Tag의 name
        :return: tag 객체 조회 혹은 추가
        """
        tag, tag_created = Tag.objects.get_or_create(name=tag_name)
        if tag_created:
            self.tags.add(tag)

    @property
    def like_count(self):
        """
        자신(Post 인스턴스)을 like하고 있는 user 수 리턴
        post.like_count 와 같이 () 없이 변수처럼 사용 가능
        """
        return self.like_users.count()


class PostLike(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User)
    created_date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(Post)
    author = models.ForeignKey(User)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(
        User,
        through='CommentLike',
        related_name='like_comments',
    )


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment)
    user = models.ForeignKey(User)
    created_date = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return 'Tag({})'.format(self.name)
