import cv2
import numpy as np
from PIL import Image
import copy


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
    ret_v=0;
    for i in range(x+1,lx+x):
        for j in range(y+1,ly+y):
            temp=fig[i,j]-(1/4)*(fig[i-1,j]+fig[i,j-1]+fig[i+1,j]+fig[i,j+1])
            ret_v=abs(ret_v+temp)
    return ret_v

"""
大小 768*768 32*32为一个block
一共12*12个block 可以嵌入144位
"""
image = cv2.imread('611_dec.png', cv2.IMREAD_GRAYSCALE) # type: ignore
#init rc4 key stream
rc4=RC4(b'115')
s0s1_mt=np.empty((768,768))
for i in range(0,768):
    for j in range(0,768):
        s0s1_mt[i][j]=int(rc4.prga()%2)

"""只需要在此处设置您的嵌入信息即可，最长不超过144位"""
emb_info=[1,0,1,0,1,0,0,1,1,1,1,0,
          1,1,0,0,0,1,0,1,0,0,0,1]

len_of_info=len(emb_info)
# print(image[0:100,0:100])

for x in range(len_of_info):
    hang=int(x/24)
    lie=x%24
    for i in range(32): 
        for j in range(32):
            p1=hang*32+i
            p2=lie*32+j
            if(emb_info[x]==1):
                if s0s1_mt[p1][p2]==1.0:
                    image[p1,p2]=image[p1,p2]^7
                else: 
                    continue
            else:
                if s0s1_mt[p1][p2]==1.0:
                    continue
                else:
                    image[p1,p2]=image[p1,p2]^7
# print(image[0:100,0:100])
image = Image.fromarray(image).convert('L')
image.show()
image.save("611_emb.png")


