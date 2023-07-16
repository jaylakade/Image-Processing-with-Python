import imp
import cv2
import numpy as np
from PIL import Image
import sys

str = str(sys.argv[1])
img = cv2.imread(str)

gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


if str[len(str)-5]=='1':
    clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize= (5,5))
    equalized_img = clahe.apply(gray_img)
    cv2.imwrite("enhanced-cctv1.jpg",equalized_img)

elif str[len(str)-5]=='2':
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize= (15,15))
    equalized_img = clahe.apply(gray_img)
    cv2.imwrite("enhanced-cctv2.jpg",equalized_img)

elif str[len(str)-5]=='3':
    clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize= (5,5))
    equalized_img = clahe.apply(gray_img)
    cv2.imwrite("enhanced-cctv3.jpg",equalized_img)

elif str[len(str)-5]=='4':
    clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize= (15,15))
    equalized_img = clahe.apply(gray_img)
    cv2.imwrite("enhanced-cctv4.jpg",equalized_img)
