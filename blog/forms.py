''' 通过form组件实现注册页面的校验,这个不会走数据库，直接前端 '''

from django import forms
from django.forms import widgets
from blog import models
from django.core.exceptions import  NON_FIELD_ERRORS,ValidationError


class RegForm(forms.Form):
    username=forms.CharField(min_length=5, # 用户名最少5位
        widget=widgets.TextInput(attrs={"class":"form-control","id":"username","placeholder":"请输入用户名"}))

    password=forms.CharField(min_length=5,
        widget=widgets.PasswordInput(attrs={"class":"form-control","id":"password","placeholder":"请输入密码"}))
    reptpwd=forms.CharField(min_length=5,
        widget=widgets.PasswordInput(attrs={"class": "form-control", "id": "reptpwd", "placeholder": "请输入确认密码"}))
    email=forms.CharField(min_length=5,
        widget=widgets.TextInput(attrs={"class": "form-control", "id": "email", "placeholder": "请输入邮箱"}))

    def clean_username(self):
        username=self.cleaned_data.get("username")
        ret=models.User.objects.filter(username=username)
        # print("---form---",ret)

        if not ret:
            return username
        else:
            raise ValidationError("该用户名已存在")

    def clean_password(self):
        password=self.cleaned_data.get("password")
        if password.isdigit():
            raise ValidationError("密码不能为纯数字")
        else:
            return password

    def clean(self):
        password = self.cleaned_data.get("password")
        reptpwd = self.cleaned_data.get("reptpwd")

        if password == reptpwd :
            return self.cleaned_data
        else:
            raise ValidationError("两次输入密码不一致")
