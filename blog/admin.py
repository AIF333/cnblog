from django.contrib import admin
from blog import models

# Register your models here.
# 注册后可在 前端admin直接查看
admin.site.register(models.Blog)
admin.site.register(models.Category)
admin.site.register(models.Article)
admin.site.register(models.ArticleDetail)
admin.site.register(models.Tag)
admin.site.register(models.Article2Tag)
admin.site.register(models.UserInfo)
