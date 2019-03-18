
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf.urls import url
from blog import  views as blog_views
from django.views.static import  serve
from cnblog import settings

# blog 单独的urls 配置  注意页面会返回第一个匹配到的，所以特例的需要写在上面
urlpatterns = [
    # path('login/', blog_views.loginCnblog), # 登录页面 auth模块有login函数，所以名字换成loginCnblog
    # url(r'^media/(?P<path>.*)$',  serve, {"document_root": settings.MEDIA_ROOT}),

    # 点赞
    url(r'^diggit/', blog_views.diggit),

    # 评论
    url(r'^comment/', blog_views.comment),

    # 回复评论
    url(r'^reply/', blog_views.reply),

    # 文章内容
    url(r'^(?P<username>\w+)/article/(?P<articleid>\d+)', blog_views.article),

    # 带查询条件的个人站点
    url(r'^(?P<username>\w+)/(?P<condition>category|tag|cret)/(?P<para>.*)',blog_views.homeSite),

    # 个人站点的有名分组 blog
    url(r'^(?P<username>\w+)/', blog_views.homeSite)



]
