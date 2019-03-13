from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    nid = models.AutoField(primary_key=True)
    nick_name = models.CharField(max_length=32, verbose_name=u'昵称', default='')
    telphone = models.CharField(max_length=11, verbose_name=u'电话号码', unique=True,null=True,blank=True)
    create_time = models.DateField(verbose_name=u'创建时间', null=True, blank=True) #null=True 允许为空，用NULL填充 ；blank 非Text类型不能填空字符串，则结合blank设置
    gender = models.CharField(max_length=6,choices=(('male', u'男'), ('female', u'女')), default='male', verbose_name=u'性别')
    address = models.CharField(max_length=100, verbose_name=u'地址')
    avatar = models.FileField(verbose_name=u'头像',upload_to="avatarDir/",default="avatarDir/AIF.png")