from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.decorators import login_required #登录验证的装饰器，只有登录了才可访问某些页面
import json

# Create your views here.

#系统首页
@login_required  #需登录才可进入首页
def index(request):
    username=request.user.username #获取当前用户的用户名
    # print('------',username,password)
    return render(request,"index.html",{"username":username}) # render 传入参数需用双引号引起

#注册页面
def regCnblog(request):
    from blog.forms import RegForm
    from django.contrib.auth.models import User
    regForm = RegForm()

    if request.is_ajax():
        regForm = RegForm(request.POST)  # 根据ajax的data实例化
        regResponse = {"user": None, "errormsg": None}  # 注册状态字典表

        if regForm.is_valid():
            # 注册成功
            print('---regForm.cleaned_data--', regForm.cleaned_data)
            username = regForm.cleaned_data.get("username")
            password = regForm.cleaned_data.get("password")
            email = regForm.cleaned_data.get("email")

            # 生成新用户，修改状态表
            newuser = User.objects.create_user(username=username, password=password, email=email)

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

    userinfo = {"username": "None", "errormsg": None} #删除状态表，需序列化后给前端ajax

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



