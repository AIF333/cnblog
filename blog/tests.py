from django.test import TestCase

# Create your tests here.
# from PIL import Image
# img=Image.new('RGB',(160,35),'red')
# print(img)

# 测试随机数字
# import random
# print(random.randint(-1,1))
# # 测试随机字符
# print(chr(65))
# print(chr(90))
# print(chr(97))
# print(chr(122))
l=[]
for i in range(48,58):
    l.append(chr(i))

# for i in range(65,91):
#     l.append(chr(i))
# for i in range(97,122):
#     l.append(chr(i))
# print(l)

# ll=list(range(65,91))+list(range(97,122))
# print(ll)
# print(ll[0],ll[1])

# for i in range(5):
#     print(i)

# from random import choice
# def getChar():
#     listChar = []
#     for i in range(6):
#         chrList = list(range(65, 91)) + list(range(97, 122)) + list(range(48, 58))
#         listChar.append(chr(choice(chrList)))
#
#     print(''.join(listChar))
#
# getChar()

# 检查字符串
strs=["123456","abcde","123bcd"]

for str in strs:
    if str.isdigit():
        print(str)