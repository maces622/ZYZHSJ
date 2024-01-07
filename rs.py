from fileinput import filename
from logging import root
import numpy as np
from PIL import Image
import os


# img=Image.open("lena.png")
# gray_img = img.convert('L')
# gray_img=gray_img.resize((768,768))
# gray_img.save("lena.png")

def fi_th(m):
    bin_point = bin(m)
    int_point = int(bin_point,2)#2进制转为10进制整数
    #因为bin()函数转换2进制不固定位数，所以使用s = "".join(f"{num:08b}")指定生成8位，但是int(s)无法转换成对应十进制，故只用s判定取反的加减操作
    print(int_point)
    s = "".join(f"{int_point:08b}")
    if(s[5] == '1'):
        int_point = int_point - 4
    else: int_point = int_point + 4

    if(s[6] == '1'):
        int_point = int_point - 2
    else: int_point = int_point + 2

    if(s[7] == '1'):
        int_point = int_point - 1
    else: int_point = int_point + 1
    print(int_point)
    return int_point


print(fi_th(8))