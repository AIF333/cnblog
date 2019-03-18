from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# 用户表，继续Django 自己的
class UserInfo(AbstractUser):
    userid = models.AutoField(primary_key=True)
    nick_name = models.CharField(max_length=32, verbose_name=u'昵称', default='')
    telphone = models.CharField(max_length=11, verbose_name=u'电话号码', unique=True,null=True,blank=True)
    create_time = models.DateField(verbose_name=u'创建时间', null=True, blank=True, auto_now_add=True) #null=True 允许为空，用NULL填充 ；blank 非Text类型不能填空字符串，则结合blank设置
    gender = models.CharField(max_length=6,choices=(('male', u'男'), ('female', u'女')), default='male', verbose_name=u'性别')
    address = models.CharField(max_length=100, verbose_name=u'地址')
    avatar = models.FileField(verbose_name=u'头像',upload_to="avatarDir/",default="avatarDir/AIF.png")

    def __str__(self):
        return self.username
# 博客表
class Blog(models.Model):
    """
    博客信息
    """
    blogid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题', max_length=64)
    site = models.CharField(verbose_name='个人博客后缀', max_length=32, unique=True)
    theme = models.CharField(verbose_name='博客主题', max_length=32)
    user = models.OneToOneField(to='UserInfo', to_field='userid',on_delete=models.CASCADE)

    def __str__(self):
        return self.title
# 博主个人文章分类表
class Category(models.Model):
    """
    博主个人文章分类表
    """
    categoryid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题', max_length=32)
    # blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')
    blog=models.ForeignKey(verbose_name="博客",to="Blog",to_field="blogid"  ,on_delete=models.CASCADE)

    def __str__(self):
        return self.title+"-->"+str(self.blog)
# 文章
class Article(models.Model):
    articleid = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=255, verbose_name='文章描述')
    read_count = models.IntegerField(default=0, verbose_name='阅读数')
    comment_count = models.IntegerField(default=0, verbose_name='评论数')
    up_count = models.IntegerField(default=0, verbose_name='点赞数')
    down_count = models.IntegerField(default=0, verbose_name='点灭数')
    category = models.ForeignKey(verbose_name='文章类型', to='Category', to_field='categoryid', null=True,on_delete=models.CASCADE)
    #create_time = models.DateField(verbose_name='创建时间')
    create_time = models.DateTimeField(verbose_name='创建时间')
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='blogid',on_delete=models.CASCADE)
    tags = models.ManyToManyField(
        to="Tag",
        through='Article2Tag',
        through_fields=('article', 'tag'),
    )

    #create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True) 这个精确到时间

    def __str__(self):
        return self.title
#  文章详细表
class ArticleDetail(models.Model):
    """
    文章详细表
    """
    articledetailid = models.AutoField(primary_key=True)
    content = models.TextField(verbose_name='文章内容')
    article = models.OneToOneField(verbose_name='所属文章', to='Article', to_field='articleid',on_delete=models.CASCADE)

    def __str__(self):
        return self.content

class Comment(models.Model):
    """
    评论表
    """
    commentid = models.BigAutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='评论文章', to='Article', to_field='articleid',on_delete=models.CASCADE)
    content = models.CharField(verbose_name='评论内容', max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    parent_comment = models.ForeignKey('self', blank=True, null=True, verbose_name='父级评论',on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='评论者', to='UserInfo', to_field='userid',on_delete=models.CASCADE)

    up_count = models.IntegerField(default=0)

    def __str__(self):
        return self.content


# 文章点赞点灭
class ArticleUpDown(models.Model):
    """
    点赞表
    """
    articleupdownid = models.AutoField(primary_key=True)
    user = models.ForeignKey(null=True,verbose_name='点赞者', to='UserInfo', to_field='userid',on_delete=models.CASCADE)
    article = models.ForeignKey(verbose_name='文章',null=True,to="Article",to_field="articleid",on_delete=models.CASCADE)
    isup = models.BooleanField(verbose_name='是否赞',default=False)

    # 设置联合约束
    class Meta:
        unique_together=("user","article")

# 评论点赞
class CommentUp(models.Model):
    """
    点赞表
    """
    commentupid = models.AutoField(primary_key=True)
    user = models.ForeignKey(verbose_name='评论者',null=True,to="UserInfo",to_field="userid",on_delete=models.CASCADE)
    comment = models.ForeignKey(verbose_name='评论内容',null=True,to="Comment",to_field="commentid",on_delete=models.CASCADE)


class Tag(models.Model):
    tagid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='blogid',on_delete=models.CASCADE)

    def __str__(self):
        return self.title+"-->"+str(self.blog)

class Article2Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='文章', to="Article", to_field='articleid',on_delete=models.CASCADE)
    tag = models.ForeignKey(verbose_name='标签', to="Tag", to_field='tagid',on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nid)