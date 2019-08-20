from captcha.fields import CaptchaField
from django import forms
from mdeditor.fields import MDTextFormField


class WriteForm(forms.Form):
    title = forms.CharField(label="文章标题", max_length=100)
    desc = forms.CharField(label="简介", max_length=100)
    content = MDTextFormField(label="文章内容")
    img = forms.FileField(label="文章图片")
    tags = forms.SelectMultiple()


class CommentsForm(forms.Form):
    content = forms.CharField(label="想说点什么", widget=forms.Textarea(attrs={'class': 'form-control'}))
    captcha = CaptchaField()

