import cv2
import numpy as np
from PIL import Image
import copy
# 创建一个3x3的二维数组
image0 = cv2.imread('./RC4/alls0huanyuan.png', cv2.IMREAD_GRAYSCALE)
image1 = cv2.imread('./RC4/alls1huanyuan.png', cv2.IMREAD_GRAYSCALE)
s=32          

for i in range(0,8):
    f0=0
    f1=0
    for u in range(1,s-1):
        for v in range(1,s-1):
            t0=int(image0[u+s*i,v+s*i])-(int(image0[u-1+s*i,v+s*i])+int(image0[u+s*i,v-1+s*i])+int(image0[u+1+s*i,v+s*i])+int(image0[u+s*i,v+1+s*i]))/4
            f0=f0+abs(t0)  
            #print(f0)         
    for u in range(1,s-1):
        for v in range(1,s-1):
            t1=int(image1[u+s*i,v+s*i])-(int(image1[u-1+s*i,v+s*i])+int(image1[u+s*i,v-1+s*i])+int(image1[u+1+s*i,v+s*i])+int(image1[u+s*i,v+1+s*i]))/4
            f1=f1+abs(t1)
            #print(f1)
    print(f0)
    print(f1)
    if f0>f1:
        print(0)
    if f0==f1:
        print(0.5)
    if f0<f1:
        print(1)