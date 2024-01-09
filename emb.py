import cv2
import numpy as np
from PIL import Image
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



"""
大小 768*768 32*32为一个block
一共12*12个block 可以嵌入144位
"""

block_size=32
len_of_info=int(768/block_size)*int(768/block_size)
len_of_block=int(768/block_size)
emb_info=[]
for i in range(len_of_info):
    emb_info.append(i%2)


image = cv2.imread('414.png', cv2.IMREAD_GRAYSCALE) # type: ignore

#init rc4 key stream
rc4=RC4(b'115')
s0s1_mt=np.empty((768,768))
for i in range(0,768):
    for j in range(0,768):
        s0s1_mt[i][j]=int(rc4.prga()%2)


for x in range(len_of_info):
    hang=int(x/len_of_block)
    lie=x%len_of_block
    for i in range(block_size): 
        for j in range(block_size):
            p1=hang*block_size+i
            p2=lie*block_size+j
            if(emb_info[x]==1):
                if s0s1_mt[p1][p2]==1:
                    image[p1,p2]=fi_th(image[p1,p2])
                else: 
                    continue
            else:
                if s0s1_mt[p1][p2]==1:
                    continue
                else:
                    image[p1,p2]=fi_th(image[p1,p2])
# print(image[0:100,0:100])
image = Image.fromarray(image)
image.show()
image.save("414_emb.png")


