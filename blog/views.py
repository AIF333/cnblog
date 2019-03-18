from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.decorators import login_required #登录验证的装饰器，只有登录了才可访问某些页面
import json

# Create your views here.

#系统首页
# @login_required  #不登录也可进入首页
def index(request):
    from blog import models
    username=request.user.username #获取当前用户的用户名
    # print('------',username,password)
    articles = models.Article.objects.all().order_by("-create_time")

    # 如果登录的用户
    if username:
        return render(request,"index.html",{"username":username,"articles":articles}) # render 传入参数需用双引号引起
    else:
        return render(request,'nologindex.html')

#注册页面
def regCnblog(request):
    from blog.forms import RegForm
    # from django.contrib.auth.models import User # 自定义了User，需将auth的替换成自己的
    from blog.models import UserInfo as User # 自定义了User，需将auth的替换成自己的
    regForm = RegForm()

    if request.is_ajax():
        regForm = RegForm(request.POST)  # 根据ajax的data实例化
        regResponse = {"user": None, "errormsg": None}  # 注册状态字典表

        #print("----",request.POST)

        if regForm.is_valid():
            # 注册成功
            print('---regForm.cleaned_data--', regForm.cleaned_data)
            print('---regForm.cleaned_data-username-', regForm.cleaned_data.get("username"))
            username = regForm.cleaned_data.get("username")
            password = regForm.cleaned_data.get("password")
            email = regForm.cleaned_data.get("email")
            avatar=request.FILES.get("upFile")

            if not avatar:#如果用户没有选择图片，则用默认图片,这个放在前端，后端不好实现
                avatar="avatarDir/AIF.jpg"
            else:
                with open("static/pictures/%s.jpg" % username , 'wb') as f:
                    for line in avatar:
                        f.write(line)

            # 生成新用户，修改状态表
            newuser = User.objects.create_user(username=username, password=password, email=email,avatar=avatar)

            if newuser:
                regResponse["user"] = username
            else:
                raise EOFError("创建新用户失败")
        else:
            # 注册失败
            print('---regForm.cleaned_data--', regForm.cleaned_data)
            print('---regForm.errors--', regForm.errors)
            regResponse["errormsg"] = regForm.errors

        return HttpResponse(json.dumps(regResponse))

        # print("------",request.POST,request.POST.get("username"))
    else:  # 正常访问
        return render(request, 'reg.html', {"regForm": regForm})  # 字典也可写错 locals()，名字要一致

#登录页面校验

# 登录页面
def loginCnblog(request):
    from django.contrib import auth #auth 用户校验模块

    # 方法一 用GET方式
    if request.is_ajax():
        user=request.GET.get('user')
        password=request.GET.get('password')
        checkpwd=request.GET.get('checkpwd')

        userIncheckpwd=request.session['checkChars'] #用户输入的验证码
        # print("+++++++++++",userIncheckpwd,"++++++++++++")
        # print("+++++",user,"++++++",password,"++++++",checkpwd,"++++++")


        # print(userIncheckpwd.upper() == checkpwd.upper())
        # print("type of userIncheckpwd",type(userIncheckpwd),type(checkpwd))

        # 检查验证码是否输入正确
        user_info={'user':None,'errmsg':None} # 定义一个字典记录用户的登录状态，需序列化后传给js
        if  userIncheckpwd.upper() == checkpwd.upper():
            validuser=auth.authenticate(username=user,password=password)
            print('-----',validuser,type(validuser)) #  yeteng <class 'django.contrib.auth.models.User'>

            if validuser:
                # 登录成功
                user_info['user']=user
                print("登录成功用户%s写入session" % user)
                auth.login(request,validuser) # login函数将登录user写入session
            else:
                user_info['errmsg'] = '用户名或密码错误'

            return HttpResponse(json.dumps(user_info))
        else:
            user_info['errmsg']='验证码输入错误'
            print(user_info)
            return HttpResponse(json.dumps(user_info))


    return  render(request,'login.html')

#生成验证码图片
def getValidImg(request):

    #方法一 打开一个本地的图片返回给前端
    # with open("static/pictures/AIF.png","rb") as f:
    #     data=f.read()

    #方法二 用PIL模块（Pillow）导入Image生成图片
    # from PIL import  Image
    # img=Image.new(mode='RGB',size=(160,35),color='red')
    # img.save(open('static/pictures/yzm.png','wb'),'png')
    # with open("static/pictures/yzm.png","rb") as f:
    #     data=f.read()

    #方法三 用IO模块将图片通过内存过渡,将不会生成中间图片
    # from PIL import Image
    # from io import BytesIO
    # f=BytesIO()
    # img=Image.new(mode='RGB',size=(160,35),color=(100,100,100))
    # img.save(f,'png')
    # data=f.getvalue()
    # print(data)

    #方法四 用random随机生成图片 并加干扰点和干扰线
    from PIL import Image,ImageDraw,ImageFont
    from io import BytesIO
    from random import randint,choice

    #获取随机颜色组合,需传入参数透明度
    def getRanColor(transparency=255):
        transparency=int(transparency)
        return (randint(-1,255),randint(-1,255),randint(-1,255),transparency)
    #获取随机字符
    def getChar():
        # chrList=list(range(65, 91)) + list(range(97, 122))+list(range(48,58))
        chrList=list(range(65, 91)) +list(range(48,58))
        char=chr(choice(chrList))
        return char

    #生成验证码框，内部颜色随机
    width,height=(160,35)
    checkCharList=[] #验证码列表
    f=BytesIO()
    img=Image.new(mode='RGBA',size=(width,height),color=getRanColor(120))

    #设置框内字体的格式和大小
    draw=ImageDraw.Draw(img,mode='RGBA')
    font=ImageFont.truetype(font="static/kumo.ttf",size=40)

    #随机写入5个字符
    # draw.text(xy=(2,2),text='AIF',fill=getRanColor(),font=font) # 参数：xy轴举例，填充文字，字体颜色
    for i in range(5):
        textchar=getChar()
        checkCharList.append(textchar)
        draw.text(xy=(15+28*i,-2),text=textchar,fill=getRanColor(),font=font)

    for i in range(300):  # 加噪点
        draw.point([randint(0, width), randint(0, height)], fill=getRanColor())
    for i in range(3):  # 加干扰线,这里通过添加多组横纵坐标实现
        x1 = randint(0, width)
        y1 = randint(0, height)
        x2 = randint(0, width)
        y2 = randint(0, height)
        x3 = randint(0, width)
        y3 = randint(0, height)

        draw.line((x1, y1, x2, y2, x3, y3), fill=getRanColor(120))

    img.save(f,'png')
    data=f.getvalue()

    checkChars=''.join(checkCharList)
    # 验证码字符串 存入session，方便别的函数访问，也可用全局变量,
    # 需注意的是session需表建立了才能用:python manage.py makemigrations   python manage.py migrate
    request.session['checkChars']=checkChars
    # print('fffffffffffffffff',f)
    # print('---------------',checkChars,'---------------',data,'----------')

    return HttpResponse(data)

#注销页面
def logoutCnblog(request):
    from django.contrib.auth import logout
    logout(request)
    return  redirect("/login/")

# 删除登录用户
@login_required  #需登录才可进入
def delUser(request):
    from django.contrib.auth.models import User

    userinfo = {"username": "None", "errormsg": None}  # 删除状态表，需序列化后给前端ajax

    if request.is_ajax():
        username=request.POST.get("username") #前端传入的用户名
        workusername=request.user.username #实际登录的使用名
        print('------',request.POST)
        print("------username--",username,'-------------',workusername)

        if username == workusername:
            user=User.objects.get(username=username)
            deluser=user.delete()

            if deluser:
                userinfo["username"]=username
            else:
                userinfo["errormsg"]="删除用户%s失败" % username
        else:
            userinfo["errormsg"] = "非本用户无权限删除"

        print(userinfo)
        return HttpResponse(json.dumps(userinfo))

#个人站点

# def homeSite(request,username,**kwargs):
def homeSite(request,username,**kwargs):
    from blog import models
    from django.db.models import Count

    # #方法一 用数据库生成的 外键字段_id 等于
    # blog=models.Blog.objects.filter(user_id=request.user.userid)
    # 方法二 直接用user对象 get方法返回的是一条记录，filter返回的则是一个set
    # blog1=models.Blog.objects.get(user=request.user)

    conditon=kwargs.get("condition")
    para=kwargs.get("para")
    # print(username,conditon,para,kwargs,"----------")
    user=models.UserInfo.objects.get(username=username)
    blog=user.blog

    # 文章的分类归档
    # 方法1 ，直接用分类的结果集,在前端渲染 归档和文章数
    catelist = models.Category.objects.filter(blog=blog)

    # # 方法二  用 count 分组函数，catelist 是分类的title和对应文章数的 QuerySet
    # catelist=models.Category.objects.filter(blog=blog).annotate(c=Count("article__articleid")).values_list("title","c")
    # print(catelist2)

    # 标签归档
    # print( "-----------")
    taglist=models.Tag.objects.filter(blog=blog).filter(article__blog=blog).values("title").annotate(c=Count("article2tag__article")).values_list("title","c")
    # print(taglist,"------")

    # 发布时间归档
    crelist=models.Article.objects.filter(blog=blog).extra(select={"formateDate":"strftime('%%Y-%%m',create_time)"})\
         .values_list("formateDate").annotate(C=Count("title")).values_list("formateDate","C")

    if not kwargs: # 如果没有输入左侧的选择，则显示用户的所有文章
        articles = models.Article.objects.filter(blog=blog).order_by("-create_time")
    elif conditon == "category": #  选择 文章分类
        # print(conditon, para, "---11111---")

        # 两种写法都可以，方法一分两步
        # catrgory=models.Category.objects.filter(title=para)
        # articles=models.Article.objects.filter(blog=blog).filter(category__in=catrgory)

        # 方法二直接一个查询
        articles=models.Article.objects.filter(blog=blog).filter(category__title=para)

    elif conditon == "tag": # 选择  标签分类
        # print(conditon, para, "---22222---")
        # tag=models.Tag.objects.filter(title=para)
        # articles =models.Article.objects.filter(blog=blog).filter(tags__in=tag)
        articles=models.Article.objects.filter(blog=blog).filter(tags__title=para)

    elif conditon == "cret" : # 选择 月份分类
        # print(conditon, para, "---33333---")
        articles=models.Article.objects.filter(blog=blog).extra(select={"formateDate": "strftime('%%Y-%%m',create_time)"})\
            .extra(where=["formateDate = '%s'"%para ])

    # 文章
    # if user.is_superuser: #超级用户可以看全部的文章 文章按时间排序
    #     # 这里注释，后期需要可以放开
    #     # articles=models.Article.objects.all().order_by("-create_time")
    #     articles = models.Article.objects.filter(blog=blog).order_by("-create_time")
    # else:
    #     # #方法一 用数据库生成的 外键字段_id 等于
    #     #  articles=models.Article.objects.filter(blog_id=blog.values_list("blogid")[0]).order_by("-create_time")
    #     # 方法二 用blog对象
    #     articles=models.Article.objects.filter(blog=blog).order_by("-create_time")
    # print("55555555555555555")
    return render(request,"homesite.html",locals())

# 文章渲染
def article(request,username,articleid):
    from blog import models

    blog=models.Blog.objects.filter(user__username=username)[0]
    print("---",blog)
    article=models.Article.objects.filter(blog=blog,articleid=articleid)[0]

    commentList=models.Comment.objects.filter(article=article)

    return render(request,"article.html",{"article":article,"commentList":commentList})

# 点赞功能
def diggit(request):
    from django.db import transaction
    from django.db.models import F
    from blog import models

    # print("diggit---------------11111")
    if request.is_ajax():
        article_id=request.POST.get("article_id")

        print(request.user.username,article_id,"-----")
        user=request.user
        article=models.Article.objects.filter(articleid=article_id)
        art_state={"state":False}
        # 在点赞表中加一个 用户和文章的记录，同时文章表的点赞数+1，这两个是事物
        try:
            with transaction.atomic():
                # 方法一
                models.ArticleUpDown.objects.create(user_id=user.userid,article_id=article_id)
                # 方法二
                # models.ArticleUpDown.objects.create(user=user,article=article[0])
                article.update(up_count=F("up_count")+1)
                art_state={"state":True}
        except:
            pass

    # django 下的json，在前端不需要反序列化
    from django.http import JsonResponse
    return JsonResponse(art_state)


# 评论功能
def comment(request):
    import datetime
    from blog import models
    from django.db import transaction
    from django.db.models import F

    if request.is_ajax():
        content=request.POST.get("comment")
        comentuser=request.user.userid
        article_id=request.POST.get("article_id")
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # print(comment,comentuser,article_id,"+++++++")

        # 做到父级评论可以到数据库了

        # 定一个中专的字典
        commentInfo = {"create_time":None}
        commentInfo["create_time"]=create_time

        with transaction.atomic():
            models.Comment.objects.create(content=content,create_time=create_time,article_id=article_id,user_id=comentuser)
            models.Article.objects.filter(articleid=article_id).update(comment_count=F("comment_count")+1)

        from django.http import JsonResponse
        import json

        # commentInfo=json.dumps(commentInfo)

    print(commentInfo,type(commentInfo),"000000")
    return JsonResponse(commentInfo)
    # return HttpResponse(commentInfo)

def reply(request):
    pass

# 测试用
def test1(request):
    from blog.models import UserInfo as User
    print('-----',request.method)
    if request.method=="POST":
        print(request.POST)
        print(request.FILES)

        myfile=request.FILES.get("myfile")
        with open("static/pictures/newf.jpg",'wb') as f:
            for line in myfile:
                f.write(line)

        return HttpResponse("Up file OK!")

    print("====",User.objects.filter(username="fandandan"))
    #print("+++++++++++",models.User.objects.filter(username="fandandan"))
    return render(request,"test1.html")




