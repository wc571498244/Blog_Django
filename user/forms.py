import re

from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form, EmailField
from django import forms

from user.models import UserProfile


class RegisterForm(ModelForm):
    repassword = forms.CharField(required=True, error_messages={'required': '必须填写密码'}, label='密码',
                                 widget=forms.widgets.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password']

    # 自定义验证用户名
    def clean_username(self):
        username = self.cleaned_data.get('username')
        result = re.match(r'[a-zA-z]\w{5,}', username)
        if not result:
            raise ValidationError('用户名必须字母开头')
        return username


class LoginForm(Form):
    username = forms.CharField(max_length=50, min_length=6, error_messages={"min_length": "用户名长度至少6位"}, label="用户名")
    password = forms.CharField(required=True, error_messages={'required': '必须填写密码'}, label='密码',
                               widget=forms.widgets.PasswordInput)
    captcha = CaptchaField()
    """
    存在不稳定因素
    class Meta:
        model = UserProfile
        fields = ['username', 'password'
    自定义验证用户名
    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = UserProfile.objects.filter(username=username).exists()
        if not user:
            raise ValidationError("用户名不存在")
        return username
    """


class forgetPasswordForm(Form):
    email = EmailField(required=True, error_messages={"required": "必须填写此字段！"},
                       widget=forms.widgets.TextInput(attrs={"class": "form-control", "placeholder": "请输入您的邮箱"}))
    captcha = CaptchaField()
