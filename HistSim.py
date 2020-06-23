# -*- coding: UTF-8 -*-
import pymysql
from PIL import Image
import os
import numpy as np
import time
import json
import sys

# 生成直方图 opencv
# def img2hist(imagefile):
#     image=cv2.imread(imagefile)
#     imgsize = 256
#     image=cv2.resize(image,(imgsize,imgsize))
#     hist = cv2.calcHist([image], [1], None, [256], [0, 256])
#     cv2.normalize(hist, hist,0,255*0.9,cv2.NORM_MINMAX)
#     return hist

# 生成直方图 PIL
def img2hist(image):
    hist=image.histogram()
    histmax=np.max(hist)
    for i in range(len(hist)):
        # 连续直方图
        hist[i]=hist[i]/histmax*255
        # 离散直方图
        # hist[i]=int(round(hist[i]/histmax*255))
    return hist

# # 直方图相交法
# def hist_match(hist_template,hist_test):
#     template_sum=sum(hist_template)
#     result=0
#     for i in range(len(hist_template)):
#         if hist_template[i]<=hist_test[i]:
#             result=result+hist_template[i]
#         else:
#             result=result+hist_test[i]
#     score=result/template_sum
#     return score

# 直方图相交法比较直方图相似度
def hist_match(hist1,hist2):
    sum1 = 0
    len1=len(hist1)
    for i in range(len1):
       if (hist1[i] == hist2[i]):
          sum1 += 1
       else:
           sum1 += 1 - float(abs(hist1[i] - hist2[i]))/ max(hist1[i], hist2[i])
    return sum1/len1
    
# 使用16进制存储直方图
def hist2hex(histarr):
    histDec=[]
    histHex=''
    histmax=np.max(histarr)
    for i in range(len(histarr)):
        histDec.append(int(round(histarr[i]/histmax*15)))
    for c in range(len(histDec)):
        hexstr=str(hex(histDec[c]))
        histHex=histHex+hexstr[2]
    return histHex

# 利用存储的16进制码重建直方图
def hex2hist(hexstr):
    histarr=[]
    for c in hexstr:
        histarr.append((int('0x'+c,16))/10*255)
    return histarr


if __name__ == "__main__":
    imgpath=sys.argv[1]
    des_path='./hist_des/'
    # 连接数据库
    conn=pymysql.connect(host="localhost",user="image_search",passwd="kyzdmbrK8hfyATry",db="image_search")
    cur=conn.cursor()
    sql="SELECT * FROM image_search.imgtable"
    cur.execute(sql)
    data=cur.fetchall()
    # 总数量，COCO2014图片集共82783
    num=len(data)
    # 测试图片
    image1 = Image.open(imgpath)
    # 转换为灰度图像
    image1 = image1.convert('L')
    # 将图像调整为统一尺寸
    imgsize = 256
    image1=image1.resize((imgsize, imgsize),Image.ANTIALIAS)
    # 获得测试图片哈希值
    hist1=img2hist(image1)
    # 计算汉明距离，寻找最佳匹配图像
    maxdiff=0
    maxindex=0
    for i in range(num):
        # 字符串转数组
        # image2 = Image.open('/www/wwwroot/tjlzt98.cn/imagesearch/coco/coco'+str(i)+'.jpg')
        # image2 = image2.convert('L')
        # image2=image2.resize((imgsize, imgsize),Image.ANTIALIAS)
        hist2=np.load(des_path+str(i)+'.npy')
        # hist2=hex2hist(data[i][3])
        # 计算汉明距离
        diff=hist_match(hist1,hist2)
        # diff=hist_match(hist1, hist2)
        # 寻找最大匹配相似度
        if(diff>maxdiff):
            maxindex=i
            maxdiff=diff
    # 最短距离
    print(str(maxdiff)+','+str(maxindex))
    # 最佳匹配图像
    # 关闭数据库
    cur.close() # 关闭游标
    conn.close() # 关闭连接