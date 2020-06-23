# -*- coding: UTF-8 -*-
import pymysql
from PIL import Image
import os
import numpy as np
import time
import json
import sys

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
        histarr.append((int('0x'+c,16))/16*255)
    return histarr


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

# 比较直方图相似度
def difference(hist1,hist2):
    sum1 = 0
    len1=len(hist1)
    for i in range(len1):
       if (hist1[i] == hist2[i]):
          sum1 += 1
       else:
           sum1 += 1 - float(abs(hist1[i] - hist2[i]))/ max(hist1[i], hist2[i])
    return sum1/len1

def hist_match(hist_template,hist_test):
    template_sum=sum(hist_template)
    result=0
    for i in range(len(hist_template)):
        if hist_template[i]<=hist_test[i]:
            result=result+hist_template[i]
        else:
            result=result+hist_test[i]
    score=result/template_sum
    return score

if __name__ == "__main__":
    conn=pymysql.connect(host="localhost",user="image_search",passwd="kyzdmbrK8hfyATry",db="image_search")
    cur=conn.cursor()
    sql="SELECT * FROM image_search.imgtable"
    cur.execute(sql)
    data=cur.fetchall()
    # 总数量，COCO2014图片集共82783
    num=len(data)
    imgsize = 256
    save_path='./hist_des/'
    for i in range(num):
        image1=Image.open('/www/wwwroot/tjlzt98.cn/imagesearch/coco/'+data[i][1])
        image1=image1.convert('L')
        image1=image1.resize((imgsize, imgsize),Image.ANTIALIAS)
        hist1=img2hist(image1)
        np.save(save_path+str(i)+'.npy',hist1)
        print(str(i)+' success')
    cur.close() # 关闭游标
    conn.close() # 关闭连接



    # retval1  = cv.compareHist(histGrayImage, histGrayPic, cv.HISTCMP_BHATTACHARYYA)