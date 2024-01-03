import imp
import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from .test import RC4
import copy
def fi_th(m):
    bin_point = bin(m)
    int_point = int(bin_point,2)#2进制转为10进制整数
    #因为bin()函数转换2进制不固定位数，所以使用s = "".join(f"{num:08b}")指定生成8位，但是int(s)无法转换成对应十进制，故只用s判定取反的加减操作
    
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

    return int_point

key=b'1'

# 计算图像的自然波动率
def cal_v(fig,x,y,lx,ly):
    ret_v=0;
    for i in range(x+1,lx+x):
        for j in range(y+1,ly+y):
            temp=fig[i,j]-(1/4)*(fig[i-1,j]+fig[i,j-1]+fig[i+1,j]+fig[i,j+1])
            ret_v=abs(ret_v+temp)
    return ret_v

root_path=os.path.abspath(os.path.join(os.getcwd(), "."))
dec_path=os.path.join(root_path,"test2.png")
img_plt=plt.imread(dec_path)
list1=0
row1=0
num=0
code_num = 0
irt_str1 = ''
pin=0
rc4=RC4(key)
rc4_key=rc4.get_key()
while(code_num != 2304):
    content1 = rc4_key[pin]
    s = "".join(f"{content1:08b}")
    irt_str1 = irt_str1 + s
    code_num = code_num + 1
irt_count = 0
irt_num =np.zeros((144,128)) #irt_num 表初始矩阵
for i in range(144):
    for j in range(128):
        irt_num[i][j] = irt_str1[irt_count]
        irt_count = irt_count + 1
while(list1 != 144):
    if(row1 != 128):
        list_last = list1 + 18
        row_last = row1 + 32
        """
        img_plt[ list1:list_last , row1:row_last]#图像划分
        irt_num[ list1:list_last , row1:row_last]#[0，1]矩阵划分
        """
        block0=copy.deepcopy(img_plt[ list1:list_last , row1:row_last])
        block1=copy.deepcopy(img_plt[ list1:list_last , row1:row_last])
        for i in range(list1,list_last):
            for j in range(row1,row_last):

                if( int(irt_num[i][j])==0): # 如果当前[0，1]矩阵中元素与嵌入数字位数相同
                    block0[i][j] = fi_th(block0[i][j]) # 取反
                else:
                    block1[i][j] = fi_th(block1[i][j])

        func0=cal_v(block0,list1,row1,18,32)
        func1=cal_v(block0,list1,row1,18,32)
        if(func0>func1):
            print(0)
        else :
            print(1)
        row1 = row1 + 32
        num = num + 1
    else:
        list1 = list1 + 18
        row1 = 0