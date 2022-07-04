from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django import forms


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(
        label='비밀번호', widget=forms.PasswordInput(attrs={'placeholder': '비밀번호'}))
    password2 = forms.CharField(label='비밀번호 재입력', widget=forms.PasswordInput(
        attrs={'placeholder': '비밀번호 재입력'}))

    class Meta:
        model = User

        fields = ['username', 'email', 'password1', 'password2']

    def clean_password2(self):
        cd = self.cleaned_data

        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('입력하신 비밀번호가 일치하지 않습니다.')

        return cd['password2']


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = '기존 비밀번호'
        self.fields['old_password'].widget.attrs.update(
            {'class': 'form-control', 'autofocus': False, })

        self.fields['new_password1'].label = '새 비밀번호'
        self.fields['new_password1'].widget.attrs.update(
            {'class': 'form-control', })

        self.fields['new_password2'].label = '새 비밀번호 확인'
        self.fields['new_password2'].widget.attrs.update(
            {'class': 'form-control', })
