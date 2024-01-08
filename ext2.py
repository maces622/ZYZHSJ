# 改进之后的提取信息方法
# 考虑了恢复快和未恢复快边界之间的平滑度差异
from operator import ipow
import cv2
import numpy as np
from PIL import Image
import copy
from operator import attrgetter

class pix:
    def __init__(self,x,y,val):
        self.x=x
        self.y=y
        self.val=val

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

def cal_v_2(fig,x,y,lx,ly):
    ret_v=0.0
    for xx in range(x,lx+x):
        for yy in range(y,ly+y-1):
            temp=abs(float(fig[xx][yy])-float(fig[xx][yy+1]))
            ret_v=ret_v+temp
    for xx in range(x,lx+x-1):
        for yy in range(y,ly+y):
            temp=abs(float(fig[xx][yy])-float(fig[xx+1][yy]))
            ret_v=ret_v+temp
    return ret_v
"""
大小 384*384 block_size*block_size为一个block
一共12*12个block 可以嵌入144位
"""
image = cv2.imread('611_emb.png', cv2.IMREAD_GRAYSCALE) # type: ignore
#init rc4 key stream
rc4=RC4(b'115')
s0s1_mt=np.empty((768,768))

for i in range(0,768):
    for j in range(0,768):
        s0s1_mt[i][j]=int(rc4.prga()%2)


"""只需要在此处设置您的嵌入信息即可，最长不超过144位"""

block_size=8
len_of_info=int(768/block_size)*int(768/block_size)
len_of_block=int(768/block_size)
emb_mtx=np.empty((len_of_block,len_of_block))
emb_info=[]
recover_bj=np.ones((len_of_block,len_of_block))
block_list=[]
for i in range(len_of_info):
    emb_info.append(i%2)
info=[]

for x in range(len_of_info):
    hang=int(x/len_of_block)
    lie=x%len_of_block
    block0=copy.deepcopy(image[hang*block_size : hang*block_size+block_size, lie*block_size: lie*block_size+block_size])
    block1=copy.deepcopy(image[hang*block_size : hang*block_size+block_size, lie*block_size: lie*block_size+block_size])
    for i in range(block_size):
        for j in range(block_size):
            p1=hang*block_size+i
            p2=lie*block_size+j
            if(s0s1_mt[p1][p2]==0):
                block0[i][j]=fi_th(block0[i][j])
            else:
                block1[i][j]=fi_th(block1[i][j])
    block_list.append(pix(hang,lie,abs(cal_v_2(block0,0,0,block_size,block_size)-cal_v_2(block1,0,0,block_size,block_size))))
    recover_bj[hang][lie]=0

sorted_list=sorted(block_list,key=attrgetter('val'),reverse=True)

"check the val 2 of block"
# for i in range(len(block_pix_lst)):
#     print(sorted_list[i].val)
for x in range(len_of_info):
    now_block=sorted_list[x]
    hang=now_block.x
    lie=now_block.y
    block0=copy.deepcopy(image[hang*block_size : hang*block_size+block_size, lie*block_size: lie*block_size+block_size])
    block1=copy.deepcopy(image[hang*block_size : hang*block_size+block_size, lie*block_size: lie*block_size+block_size])
    for i in range(block_size):
        for j in range(block_size):
            p1=hang*block_size+i
            p2=lie*block_size+j
            if(s0s1_mt[p1][p2]==0):
                block0[i][j]=fi_th(block0[i][j])
            else:
                block1[i][j]=fi_th(block1[i][j])
    # print(block0)

    base_val_0=cal_v_2(block0,0,0,block_size,block_size)
    base_val_1=cal_v_2(block1,0,0,block_size,block_size)
    if hang-1>=0: # up hang
        if recover_bj[hang-1][lie]:
            for t in range(block_size-1):
                base_val_0=base_val_0+abs(float(image[hang*block_size-1][t+lie*block_size+1])-float(image[hang*block_size-1][t+lie*block_size]))
                base_val_1=base_val_1+abs(float(image[hang*block_size-1][t+lie*block_size+1])-float(image[hang*block_size-1][t+lie*block_size]))
            for t in range(block_size):
                base_val_0=base_val_0+abs(float(image[hang*block_size-1][t+lie*block_size])-float(block0[0][t]))
                base_val_1=base_val_1+abs(float(image[hang*block_size-1][t+lie*block_size])-float(block1[0][t]))
    
    if hang +1 <len_of_block:
        if recover_bj[hang+1][lie]:
            for t in range(block_size-1):
                base_val_0=base_val_0+abs(float(image[(hang+1)*block_size][t+lie*block_size+1])-float(image[(hang+1)*block_size][t+lie*block_size]))
                base_val_1=base_val_1+abs(float(image[(hang+1)*block_size][t+lie*block_size+1])-float(image[(hang+1)*block_size][t+lie*block_size]))
            for t in range(block_size):
                base_val_0=base_val_0+abs(float(image[(hang+1)*block_size][t+lie*block_size])-float(block0[block_size-1][t]))
                base_val_1=base_val_1+abs(float(image[(hang+1)*block_size][t+lie*block_size])-float(block1[block_size-1][t]))
    if lie -1 >=0 :
        if recover_bj[hang][lie-1]:
            for t in range(block_size-1):
                base_val_0=base_val_0+abs(float(image[t+hang*block_size+1][lie*block_size-1])-float(image[t+hang*block_size][lie*block_size-1]))
                base_val_1=base_val_1+abs(float(image[t+hang*block_size+1][lie*block_size-1])-float(image[t+hang*block_size][lie*block_size-1]))
            for t in range(block_size):
                base_val_0=base_val_0+abs(float(image[t+hang*block_size][lie*block_size-1])-float(block0[t][0]))
                base_val_1=base_val_1+abs(float(image[t+hang*block_size][lie*block_size-1])-float(block1[t][0]))
        
    if lie +1 <len_of_block :
        if recover_bj[hang][lie+1]:
            for t in range(block_size-1):
                base_val_0=base_val_0+abs(float(image[t+hang*block_size+1][(lie+1)*block_size])-float(image[t+hang*block_size][(lie+1)*block_size]))
                base_val_1=base_val_1+abs(float(image[t+hang*block_size+1][(lie+1)*block_size])-float(image[t+hang*block_size][(lie+1)*block_size]))
            for t in range(block_size):
                base_val_0=base_val_0+abs(float(image[t+hang*block_size][(lie+1)*block_size])-float(block0[t][block_size-1]))
                base_val_1=base_val_1+abs(float(image[t+hang*block_size][(lie+1)*block_size])-float(block1[t][block_size-1]))
    recover_bj[hang][lie]=1
    if(base_val_0<base_val_1):
        image[hang*block_size : hang*block_size+block_size, lie*block_size: lie*block_size+block_size]=block0[0:block_size,0:block_size]
        emb_mtx[hang][lie]=0
    else:
        image[hang*block_size : hang*block_size+block_size, lie*block_size: lie*block_size+block_size]=block1[0:block_size,0:block_size]
        emb_mtx[hang][lie]=1
    


# print("try:",info)
# print("ans:",emb_info)
for a in range(len_of_block):
    for b in range(len_of_block):
        info.append(emb_mtx[a][b])
cnterr=0;
for i in range(len_of_info):
    if(info[i]==emb_info[i]):
        continue
    cnterr=cnterr+1
# image = Image.fromarray(image).convert('L')
# image.show()
# image.save("4_emb.png")
print(float(cnterr)/float(len_of_info))

