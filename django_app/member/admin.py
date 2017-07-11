from django.contrib import admin

from .models import User

# TODO 새롭게 생성한 User 모델을 admin에 등록
admin.site.register(User)
