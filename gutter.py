from PIL import Image,ImageFilter
import pandas as pd
import numpy as np
import cv2
import sys

def get_median_blur_img(img, mmedian_kernel):
    kernel_size = [len(median_kernel),len(median_kernel)]
    width_img,height_img = img.shape
    
    median_blur_img = np.zeros([width_img - 2, height_img-2])    
    for i in range(width_img - 2):
        for j in range(height_img-2):

            ker_output = np.zeros(kernel_size)
            for k in range(kernel_size[0]):
                for l in range(kernel_size[1]):
                    ker_output[k,l] = img[k+i, l+j]
                    
            temp_ker = np.sum(median_kernel*ker_output)
            temp_ker = temp_ker/9
            median_blur_img[i, j] = temp_ker

    # cv2.imshow("gauss_blur_img.JPG", gauss_blur_img)
    # cv2.waitKey(0)
    return median_blur_img

def get_gamma_correction(img, gamma_value):
    inv_gamma = 1 / gamma_value
    gamma_graph = [((i / 255) ** inv_gamma) * 255 for i in range(256)]
    gamma_graph = np.array(gamma_graph, np.uint8)

    return cv2.LUT(img, gamma_graph)

def dilate_erode_dilate(img, d1 = 1, er = 2, d2 = 1):
    for i in range(d1):
        img = cv2.dilate(img,cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)),iterations=1)
    
    for i in range(er):
        img = cv2.erode(img,cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)),iterations=1)

    for i in range(d2):
        img = cv2.dilate(img,cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)),iterations=1)    
    return img

str = str(sys.argv[1])
    
img = cv2.imread(str)
# print(img.mode)
# cv2.imshow("original_img",img)

gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imshow("GrayImage",gray_img)

dilated_img = cv2.dilate(gray_img, np.ones((7,7), np.uint8))
# cv2.imshow("DilatedImage",dilated_img)


# median blur
median_kernel = [[1,1,1],[1,1,1],[1,1,1]]
median_kernel = np.array(median_kernel)

bg_img = get_median_blur_img(dilated_img,median_kernel)
bg_img = np.pad(bg_img, 1, 'constant', constant_values=255)
# bg_img = cv2.medianBlur(dilated_img, 21)
# print(type(dilated_img),type(bg_img))

width,height = bg_img.shape
# cv2.imshow("bg_img",bg_img)


# print(gray_img.shape)

# dif_img = np.ndarray(cv2.absdiff(gray_img, bg_img))
# cv2.imshow("dif_img",dif_img)

inv_diff_img = np.copy(gray_img)
#cv2.imshow("k",gray_img)
#cv2.waitKey(0)
for i in range(width):
    for j in range(height):
        inv_diff_img[i,j] =255 - abs(gray_img[i,j] - bg_img[i,j])

# inv_diff_img = 255 - inv_diff_img

# for i in range(width):
#     for j in range(height):
#         if inv_diff_img[i][j]>210:
#             inv_diff_img[i][j]=255
#         else :
#             inv_diff_img[i][j]=0

# cv2.imshow("diff_img",inv_diff_img)
# cv2.imshow("inv_dif_img",inv_dif_img)


# cv2.imshow("dilated_img",dilated_img)

# adeptive_thersold_img =255 - cv2.adaptiveThreshold(inv_diff_img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,21,18)
# cv2.imwrite("cleaned-gutter_adeptive.jpg",adeptive_thersold_img)

# eroded_img = cv2.erode(diff_img, np.ones((3,3), np.uint8))
# dilated_img = cv2.dilate(diff_img, np.ones((3,3), np.uint8))
# cv2.imshow("eroded_img",eroded_img)
# cv2.imshow("adeptive_thersold_img",adeptive_thersold_img)
# adeptive_thersold_img = dilate_erode_dilate(img,d1=0,d2=0,er=1)
# print(str[len(str)-5])
if str[len(str)-5]=='1':
    gamma_img = get_gamma_correction(inv_diff_img,0.7)
    cv2.imwrite("cleaned-gutter.jpg",gamma_img)

elif str[len(str)-5]=='2': 
    # count = 0
    for i in range(width):
        for j in range(height):
            if gray_img[i][j]<70:
                # count=count+1 
                inv_diff_img[i][j]= 75
            elif 70<=gray_img[i][j] <=80:
                inv_diff_img[i][j] = 80
    # print(count)
    cv2.imwrite("cleaned-gutter.jpg",inv_diff_img)
 
elif str[len(str)-5]=='3':
    adeptive_thersold_img =255 - cv2.adaptiveThreshold(inv_diff_img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,21,18)
    cv2.imwrite("cleaned-gutter.jpg",adeptive_thersold_img)   

# gamma_img = get_gamma_correction(inv_diff_img,0.7)
# cv2.imshow("gamma_img",gamma_img)
# cv2.waitKey(0)

# cv2.imwrite("cleaned-gutter.jpg",inv_diff_img)

# width,height = img.size
# print(width,height)
# print(img.mode)
# img_data = img.load()

# for i in range(height):
#     for j in range(width):
#         r,g,b = img_data[j,i]
#         if r>200 and g>200 and b>200:
#             r=255
#             g=255
#             b=255
#         img_data[j,i] = r,g,b

# img.save('test3.jpg')