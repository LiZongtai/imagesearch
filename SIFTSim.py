# -*- coding: UTF-8 -*-
import pymysql
import cv2 
import os
import numpy as np
import time
import json
import sys

def SIFT_des(img):
    r=128
    sift=cv2.xfeatures2d.SURF_create()
    img=cv2.resize(img, (r, r), interpolation=cv2.INTER_CUBIC)
    gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kp,des=sift.detectAndCompute(img, None)  # des描述子
    return des

if __name__ == "__main__":
    imgpath=sys.argv[1]
    des_path='./sift_des/'
    start=time.time()
    # 连接数据库
    conn=pymysql.connect(host="localhost",user="image_search",passwd="kyzdmbrK8hfyATry",db="image_search")
    cur=conn.cursor()
    sql="SELECT * FROM image_search.phashtable"
    cur.execute(sql)
    data=cur.fetchall()
    # 总数量，COCO2014图片集共82783
    num=len(data)
    # num=1000
    # num=2
    # 测试图片
    img1=cv2.imread(imgpath)
    # 获得测试图片特征描述值
    des1=SIFT_des(img1)
    # 计算满足匹配率的匹配点距离，寻找最佳匹配图像
    match_num_max=0
    match_max_index=0
    for i in range(num):
        # 字符串转数组
        try:
            des2=np.load(des_path+data[i][1]+'.npy')
        except:
            continue
        if len(des2)<=match_num_max:
            continue
        # bruteforce匹配
        bf=cv2.BFMatcher()
        matches=bf.knnMatch(des1, des2, k=2)
        # 寻找最小欧氏距离
        match_num=0
        # match_point=[]
        match_ratio=0.76
        for m,n in matches:
            if m.distance < match_ratio*n.distance:
                # match_point.append([m])
                match_num=match_num+1
        # match_num=len(match_point)
        if match_num>match_num_max:
            match_num_max=match_num
            match_max_index=i
    # 最短距离
    print(str(match_num_max)+','+str(match_max_index))
    # 最佳匹配图像
    # 关闭数据库
    end=time.time()
    print(end-start)
    cur.close() # 关闭游标
    conn.close() # 关闭连接