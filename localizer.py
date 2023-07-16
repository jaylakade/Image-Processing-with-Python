import cv2
import numpy
import sys


str = str(sys.argv[1])
img = cv2.imread(str)

# img = cv2.imread("s1.png")
height,length,c = img.shape

d1=0
d2=0
for i in range(height):
    for j in range(length):
        b,g,r = img[i][j]
        # print(b,g,r)
        # print(d1)
        d1 = d1 + abs(int(g) - int(b))/(height*length)
        d2 = d2 + abs(2*int(g) - int(r) -int(b))/(height*length)

        # d1 = d1/(win_size**2)
        # d2 = d2/(win_size**2)

# print(d1,d2)
if((0<=d1 and d1<=80)and(12<=d2 and d2<=85)): 
    print(2)

elif((6<d1 and d1<=20)and(0<=d2 and d2<=12)): 
    print(3)

elif((0<=d1 and d1<=6)and(1<=d2 and d2<=8)): 
    print(1)
else :
    print(0)