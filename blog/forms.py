''' 通过form组件实现注册页面的校验 '''

from django import forms
from django.forms import widgets

class RegForm(forms.Form):
    username=forms.CharField(min_length=5, # 用户名最少5位
        widget=widgets.TextInput(attrs={"class":"form-control","id":"username","placeholder":"请输入用户名"}))

    password=forms.CharField(min_length=5,
        widget=widgets.PasswordInput(attrs={"class":"form-control","id":"password","placeholder":"请输入密码"}))
    reptpwd=forms.CharField(min_length=5,
        widget=widgets.PasswordInput(attrs={"class": "form-control", "id": "reptpwd", "placeholder": "请输入确认密码"}))
    email=forms.CharField(min_length=5,
        widget=widgets.TextInput(attrs={"class": "form-control", "id": "email", "placeholder": "请输入邮箱"}))

