# -*- coding: UTF-8 -*-
import pymysql
from PIL import Image
import os
import numpy as np
import time
import json
import sys

def pHash(image,length=8,width=8):
    image = np.array(image.resize((length, width), Image.ANTIALIAS).convert('L'), 'f')
    A = []
    for i in range(0, 8):
        for j in range(0, 8):
            if i == 0:
                a = np.sqrt(1/8)
            else:
                a = np.sqrt(2/8)
            A.append(a*np.cos(np.pi*(2*j+1)*i/(2*8)))
    dct = np.dot(np.dot(image, np.reshape(A, (8, 8))), np.transpose(image))
    b = dct[0:8][0:8]
    hash = []
    avreage = np.mean(b)
    for i in range(8):
        for j in range(8):
            if b[i, j] >= avreage:
                hash.append(1)
            else:
                hash.append(0)
    return hash

def Hamming_distance(hash1, hash2):
    dist = 0
    for index in range(len(hash1)):
        if hash1[index] != hash2[index]:
            dist += 1
    return dist

if __name__ == "__main__":
    imgpath=sys.argv[1]
    # 连接数据库
    conn=pymysql.connect(host="localhost",user="image_search",passwd="kyzdmbrK8hfyATry",db="image_search")
    cur=conn.cursor()
    sql="SELECT * FROM image_search.phashtable"
    cur.execute(sql)
    data=cur.fetchall()
    # 总数量，COCO2014图片集共82783
    num=len(data)
    # 测试图片
    image1 = Image.open(imgpath)
    # 转换为灰度图像
    image1 = image1.convert('L')
    # 将图像调整为统一尺寸
    imgsize = 800
    image1=image1.resize((imgsize, imgsize),Image.ANTIALIAS)
    # 获得测试图片哈希值
    hash1=pHash(image1)
    # 计算汉明距离，寻找最佳匹配图像
    mindist=64
    minindex=0
    for i in range(num):
        # 字符串转数组
        hash2=[]
        for c in data[i][2]:
            hash2.append(int(c))
        # 计算汉明距离
        dist=Hamming_distance(hash1, hash2)
        # 寻找最小汉明距离
        if(dist<mindist):
            minindex=i
            mindist=dist
    # 最短距离
    print(str(mindist)+','+str(minindex))
    # 最佳匹配图像
    # 关闭数据库
    cur.close() # 关闭游标
    conn.close() # 关闭连接