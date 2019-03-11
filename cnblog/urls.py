"""cnblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blog import  views as blog_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', blog_views.loginCnblog), # 登录页面 auth模块有login函数，所以名字换成loginCnblog
    path('getValidImg/',blog_views.getValidImg), #生成验证码
    path('index/',blog_views.index), #首页
    path('logout/',blog_views.logoutCnblog), #注销页面
    path('reg/',blog_views.regCnblog), #注册页面 生成新用户
    path('delUser/',blog_views.delUser) #注册页面 生成新用户


]
