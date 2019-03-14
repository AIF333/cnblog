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
from django.urls import include
from django.conf.urls import url
from blog import  views as blog_views
from django.views.static import  serve
from cnblog import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', blog_views.loginCnblog), # 登录页面 auth模块有login函数，所以名字换成loginCnblog
    path('getValidImg/',blog_views.getValidImg), #生成验证码
    path('index/',blog_views.index), #首页
    path('logout/',blog_views.logoutCnblog), #注销页面
    path('reg/',blog_views.regCnblog), #注册页面 生成新用户
    path('delUser/',blog_views.delUser), #注册页面 生成新用户
    path('test/',blog_views.test1), #注册页面 上传图片，测试用，后期融入注册页面

    # 用户行为的upload配置，设置了可在页面访问 statict的django默认做了处理
    # 这个必须用 url 模块，不能用path
    #path('media/(?P<path>.*)$',serve, {'document_root': settings.MEDIA_ROOT})
    url(r'^media/(?P<path>.*)$',  serve, {"document_root": settings.MEDIA_ROOT}),

    # blog
    url(r'^blog/',include("blog.urls")),




]
