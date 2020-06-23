import numpy as np
from cv2 import cv2
import time
import os
 
if __name__ == '__main__':
    db_path = './coco/'
    save_path='./sift_des/'
    N=82783
    r=128 #resize 后的大小
    sift = cv2.xfeatures2d.SURF_create()
    # 从搜索库中进行计算
    sort_list = []
    for i in range(N):
        #图像2
        img = cv2.imread(db_path+'coco'+str(i)+'.jpg')
        img = cv2.resize(img, (r, r), interpolation=cv2.INTER_CUBIC)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度处理图像
        kp, des = sift.detectAndCompute(img, None)  # des是描述子
        np.save(save_path+'coco'+str(i)+'.jpg'+'.npy',des)