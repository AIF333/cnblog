
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf.urls import url
from blog import  views as blog_views
from django.views.static import  serve
from cnblog import settings

# blog 单独的urls 配置
urlpatterns = [
    # path('login/', blog_views.loginCnblog), # 登录页面 auth模块有login函数，所以名字换成loginCnblog
    # url(r'^media/(?P<path>.*)$',  serve, {"document_root": settings.MEDIA_ROOT}),

    # blog
    url(r'^(.+)/',blog_views.homeSite),




]
