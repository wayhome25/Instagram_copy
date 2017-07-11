from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):

    # todo label 뒤의 ':'를 삭제한다
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': '사용쟈 아이디를 입력하세요',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '비밀번호를 입력하세요',
            }
        )
    )

    # is_valid 실행 시 Form 내부의 모든 Field에 대한 유효성 검증을 실행하는 메서드
    # https: // docs.djangoproject.com / en / 1.11 / ref / forms / validation /
    def clean(self):
        # clean() 메서드를 실행한 기본결과 dict를 가져옴
        # cleaned_data = super().clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        user = authenticate(username=username, password=password)

        # 인증에 성공한 경우 Form의 cleaned_data의 'user' 키에 인증된 User 객체를 할당
        if user is not None:
            self.cleaned_data['user'] = user

        # 인증에 실패한 경우 is_valid()를 통과하지 못하도록 ValidationError 발생
        else:
            raise forms.ValidationError('로그인 정보에 문제가 있습니다')

        return self.cleaned_data
