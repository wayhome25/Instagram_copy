from django import forms

from ..models import Post


class PostForm(forms.ModelForm):
    # 생성자를 조작해서 Post 모델의 photo 필드는 blank=True 이지만
    # Form을 사용할 때는 반드시 photo를 받도록 함
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].required = True

    comment = forms.CharField(required=False, widget=forms.TextInput)

    class Meta:
        model = Post
        fields = ('photo', 'comment')
