import cv2
import numpy as np
import sys


# original = cv2.imread("original.jpg")
# print(original.shape)

str_y = sys.argv[1]
str_cb = sys.argv[2]
str_cr = sys.argv[3]

y = cv2.imread(str_y,0)
cr = cv2.imread(str_cr,0)
cb = cv2.imread(str_cb,0)

height,length = y.shape
# print(y.shape)

img = np.zeros((height,length,3),np.uint8)

for i in range(height):
    for j in range(length):
        img[i][j][0]=int(y[i][j])
        img[i][j][1]=int(cr[int(i/4)][int(j/4)])
        img[i][j][2]=int(cb[int(i/4)][int(j/4)])

        # print(img[i][j])

img = cv2.cvtColor(img,cv2.COLOR_YCrCb2BGR)
img = cv2.bilateralFilter(img,5,8,12)

# print(img[0][0][2])

# cv2.imshow("output",img)
cv2.imwrite("flyingelephant.jpg",img)
cv2.waitKey(0)

# print(y.shape)
# print(cr.shape)
# print(cb.shape)
