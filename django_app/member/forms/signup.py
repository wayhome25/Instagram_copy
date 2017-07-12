from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()

class SignupForm(forms.Form):
    """
    SignupForm을 구성하고 해당 form을 view에서 사용하도록 설정
    """
    username = forms.CharField(
        help_text='회원가입 help_text 테스트',
        widget=forms.TextInput
    )
    nickname = forms.CharField(
        widget=forms.TextInput,
        help_text='닉네임은 유일해야 합니다',
        max_length=24,
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput
    )

    # clean_<filedname> 메서드를 사용해서 username 필드에 대한 유효성 검증 실행
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exist')
        return username

    # nickname 유일한지 검증
    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if nickname and User.objects.filter(nickname=nickname).exitsts():
            raise forms.ValidationError('닉네임이 이미 존재합니다.')
        return nickname

    # password 1, 2 가 같은지 검증
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('비밀번호 불일치!')
        return password2

    # cleaned_data 를 사용하여 유저 생성 및 반환
    def create_user(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password2']
        nickname = self.cleaned_data['nickname']
        return User.objects.create_user(
            username=username,
            nickname=nickname,
            password=password,
        )