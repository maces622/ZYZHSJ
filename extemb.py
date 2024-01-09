import cv2
import numpy as np
from PIL import Image
import copy
import time
start_time = time.time()

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

class RC4:
    def __init__(self, key=None):
        self.state = list(range(256))  # Initialize state array
        self.x = self.y = 0  # Set indices to 0

        # Key-scheduling algorithm (KSA)
        if key:
            self.init_ksa(key)

    def init_ksa(self, key):
        j = 0
        for i in range(256):
            j = (j + self.state[i] + key[i % len(key)]) % 256
            self.state[i], self.state[j] = self.state[j], self.state[i]
    def prga(self):  # Pseudo-random generation algorithm (PRGA)
        self.x = (self.x + 1) % 256
        self.y = (self.y + self.state[self.x]) % 256
        self.state[self.x], self.state[self.y] = self.state[self.y], self.state[self.x]
        return self.state[(self.state[self.x] + self.state[self.y]) % 256]


def cal_v(fig,x,y,lx,ly):
    ret_v=0.0;
    for i in range(x+1,lx+x-1):
        for j in range(y+1,ly+y-1):
            temp=float(fig[i][j])-float(fig[i-1][j]/4+fig[i-1][j]/4+fig[i][j-1]/4+fig[i][j+1]/4)
            ret_v=ret_v+abs(temp)
    return ret_v

"""
大小 384*384 block_size*block_size为一个block
一共12*12个block 可以嵌入144位
"""
image = cv2.imread('414_emb.png', cv2.IMREAD_GRAYSCALE) # type: ignore
#init rc4 key stream
rc4=RC4(b'115')
s0s1_mt=np.empty((768,768))
for i in range(0,768):
    for j in range(0,768):
        s0s1_mt[i][j]=int(rc4.prga()%2)


"""只需要在此处设置您的嵌入信息即可，最长不超过144位"""

block_size=32
len_of_info=int(768/block_size)*int(768/block_size)
len_of_block=int(768/block_size)
emb_info=[]
for i in range(len_of_info):
    emb_info.append(i%2)
info=[]
for x in range(len_of_info):
    hang=int(x/len_of_block)
    lie=x%len_of_block
    blocka=copy.deepcopy(image[hang*block_size : hang*block_size+block_size, lie*block_size: lie*block_size+block_size])
    blockb=copy.deepcopy(image[hang*block_size : hang*block_size+block_size, lie*block_size: lie*block_size+block_size])
    for i in range(block_size):
        for j in range(block_size):
            p1=hang*block_size+i
            p2=lie*block_size+j
            if(s0s1_mt[p1][p2]==0):
                blocka[i][j]=fi_th(blocka[i][j])
            else:
                blockb[i][j]=fi_th(blockb[i][j])
    # print(blocka)
    # print(blockb)
    # break;
    f_val_a=cal_v(blocka,0,0,block_size,block_size)
    f_val_b=cal_v(blockb,0,0,block_size,block_size)
    # print(f_val_a,f_val_b)
    if(f_val_a>f_val_b):
        # print(1)
        info.append(1)
    else :
        # print(0)
        info.append(0)
# print("try:",info)
# print("ans:",emb_info)
errorbj=copy.deepcopy(image[0:768,0:768])
cnterr=0;
for i in range(len_of_info):
    if(info[i]==emb_info[i]):
        continue
    h=int(i/len_of_block)
    l=i%len_of_block
    for x1 in range(block_size):
        for x2 in range(block_size):
            errorbj[h*block_size+x1][l*block_size+x2]=0
    cnterr=cnterr+1

errorbj = Image.fromarray(errorbj)
errorbj.show()
errorbj.save("fault.png")

# image = Image.fromarray(image).convert('L')
# image.show()
# image.save("4_emb.png")
print(float(cnterr)/float(len_of_info))

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Execution time: {elapsed_time} seconds")