from django.shortcuts import render,HttpResponse

# Create your views here.



#登录首页
def login(request):
    return  render(request,'login.html')

#生成验证码图片
def getValidImg(request):

    #方法一 打开一个本地的图片返回给前端
    # with open("staticAIF/pictures/AIF.png","rb") as f:
    #     data=f.read()

    #方法二 用PIL模块（Pillow）导入Image生成图片
    # from PIL import  Image
    # img=Image.new(mode='RGB',size=(160,35),color='red')
    # img.save(open('staticAIF/pictures/yzm.png','wb'),'png')
    # with open("staticAIF/pictures/yzm.png","rb") as f:
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
        chrList=list(range(65, 91)) + list(range(97, 122))+list(range(48,58))
        # char=str(chr(choice(chrList)))
        char=chr(choice(chrList))
        return char

    #生成验证码框，内部颜色随机
    width,height=(160,35)
    f=BytesIO()
    img=Image.new(mode='RGBA',size=(width,height),color=getRanColor(100))

    #设置框内字体的格式和大小
    draw=ImageDraw.Draw(img,mode='RGBA')
    font=ImageFont.truetype(font="staticAIF/kumo.ttf",size=38)

    #随机写入5个字符
    # draw.text(xy=(2,2),text='AIF',fill=getRanColor(),font=font) # 参数：xy轴举例，填充文字，字体颜色
    for i in range(5):
        draw.text(xy=(15+28*i,-2),text=getChar(),fill=getRanColor(),font=font)

    for i in range(100):  # 加噪点
        draw.point([randint(0, width), randint(0, height)], fill=getRanColor())
    for i in range(3):  # 加干扰线,这里通过添加多组横纵坐标实现
        x1 = randint(0, width)
        y1 = randint(0, height)
        x2 = randint(0, width)
        y2 = randint(0, height)
        x3 = randint(0, width)
        y3 = randint(0, height)

        draw.line((x1, y1, x2, y2, x3, y3), fill=getRanColor(150))

    img.save(f,'png')
    data=f.getvalue()
    return HttpResponse(data)
