"""
用于将上一层目录中的picture文件夹中的jpg数据集文件转为png灰度图像
处理图像请使用png格式,jpg格式会导致多次保存后的数据丢失
"""
from fileinput import filename
from logging import root
import numpy as np
from PIL import Image
import os

# 读取目录
root_path=os.path.abspath(os.path.join(os.getcwd(), ".."))
pic_path=os.path.join(root_path,"picture")
files=os.listdir(pic_path)
gray_path=os.path.join(root_path,"gray_pic")
print(gray_path)
for file in files:
    original_image_path=os.path.join(pic_path,file)
    file_name = os.path.splitext(file)[0]
    # print(file_name)
    if original_image_path.lower().endswith(('.jpg')):
        try:
            with Image.open(original_image_path) as img:
                gray_img = img.convert('L')
                gray_img=gray_img.resize((768,768))
                gray_img.save(os.path.join(gray_path,file_name+".png"))
        except Exception as e:
            print("无法打开",file_name)
            pass
        

