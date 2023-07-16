from operator import le
import cv2
import numpy as np
import sys
import math

def get_gaussian_blur_img(img, gauss_kernel):
    kernel_size = [len(gauss_kernel),len(gauss_kernel)]
    width_img,height_img = img.shape
    
    gauss_blur_img = np.zeros([width_img - 2, height_img-2])    
    for i in range(width_img - 2):
        for j in range(height_img-2):

            ker_output = np.zeros(kernel_size)
            for k in range(kernel_size[0]):
                for l in range(kernel_size[1]):
                    ker_output[k,l] = img[k+i, l+j]
                    
            temp_ker = np.sum(gauss_kernel*ker_output)
            temp_ker = temp_ker/16
            gauss_blur_img[i, j] = temp_ker

    # cv2.imshow("gauss_blur_img.JPG", gauss_blur_img)
    # cv2.waitKey(0)
    return gauss_blur_img

def get_gradient_img(img, grad_x_kernel, grad_y_kernel):
    kernel_size = [len(grad_x_kernel),len(grad_y_kernel)]
    width_img,height_img = img.shape

    grad_img = np.zeros([width_img - 2, height_img-2])
    
    for i in range(width_img - 2):
        for j in range(height_img-2):
            
            ker_output = np.zeros(kernel_size)
            for k in range(kernel_size[0]):
                for l in range(kernel_size[1]):
                    ker_output[k,l] = img[k+i, l+j]
                    
            temp_ker1 = np.sum(grad_x_kernel*ker_output) / 8
            temp_ker2 = np.sum(grad_y_kernel*ker_output) / 8
            grad_img[i, j] = np.sqrt(temp_ker1**2 + temp_ker2**2)
            
    # cv2.imshow("gradient_img.JPG", grad_img)
    # cv2.waitKey(0)
    return grad_img

def get_laplace_img(img, lap_kernel):
    kernel_size = [len(lap_kernel),len(lap_kernel)]
    width_img,height_img = img.shape
    
    lap_img = np.zeros([width_img - 2, height_img-2])
    
    for i in range(width_img -  2):
        for j in range (height_img-2):
            
            ker_output = np.zeros(kernel_size)
            for k in range(kernel_size[0]):
                for l in range(kernel_size[1]):
                    ker_output[k,l] = img[k+i, l+j]
                    
            temp_ker = np.sum(lap_kernel*ker_output)
            lap_img[i, j] = temp_ker
    
    # cv2.imshow("laplace_img.JPG", lap_img)
    # cv2.waitKey(0)
    return lap_img  

def get_hysteresis_img(img,thresh1,thresh2):
    width_img,height_img = img.shape

    high_thresh = np.where(img > thresh1)
    low_thresh = np.where(img < thresh2)
    img[high_thresh] = 255
    img[low_thresh] = 0
    
    for i in range(1, width_img - 1):
        for j in range(1, height_img - 1):
            if(img[i, j] > thresh1 and img[i,j] < thresh2):
                temp_ker = max(img[i+1, j], img[i-1, j], img[i, j+1], img[i, j-1])
                if(temp_ker == 255):
                    img[i, j] = 255
                else:
                    img[i,j] = 0

    # cv2.imshow("hysteresis_img", img)
    # cv2.waitKey(0)
    return img

def get_dilate_erode_dilate_img(img, d1 = 1, er = 2, d2 = 1):
    for i in range(d1):
        img = cv2.dilate(img,cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)),iterations=1)
    
    for i in range(er):
        img = cv2.erode(img,cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)),iterations=1)

    for i in range(d2):
            img = cv2.dilate(img,cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)),iterations=1)    
    return img

def canny_edge_detector(img,thresh1,thresh2):
    #gaussian kernel matrix
    gauss_kernel = [[1,2,1],[2,4,2],[1,2,1]]
    gauss_kernel = np.array(gauss_kernel)

    gauss_blur_img = get_gaussian_blur_img(img, gauss_kernel)
    gauss_blur_img = get_gaussian_blur_img(gauss_blur_img, gauss_kernel)

    #gradient kernel matrix
    grad_x_kernel = [[1,0,-1],[2,0,-2],[1,0,-1]]
    grad_x_kernel = np.array(grad_x_kernel)
    grad_y_kernel = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]
    grad_y_kernel = np.array(grad_y_kernel)

    grad_img = get_gradient_img(gauss_blur_img, grad_x_kernel,grad_y_kernel)

    #laplace kernel matrix
    lap_kernel = [[0,1,0],[1,-4,1],[0,1,0]]
    lap_kernel = np.array(lap_kernel)

    lap_img = get_laplace_img(grad_img, lap_kernel)

    img = get_gaussian_blur_img(lap_img, gauss_kernel)
    img = get_gaussian_blur_img(img, gauss_kernel)
    img = get_gaussian_blur_img(img, gauss_kernel)
    img = np.uint8(get_gaussian_blur_img(lap_img, gauss_kernel))

    #hysteresis 
    hysteresis_img = get_hysteresis_img(img,thresh1,thresh2)

    # cv2.imshow("hystersis_img.jpg",hysteresis_img)
    # cv2.waitKey(0)
    return hysteresis_img

def get_probabilistic_hough_line_transform(img):
    return 

str = str(sys.argv[1])
img = cv2.imread(str)
gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
canny_edge_img = canny_edge_detector(gray_img,100,150)

# canny_edge_img = get_dilate_erode_dilate_img(canny_edge_img,2,3,1)

# cv2.imwrite("canny_edge_img.jpg",canny_edge_img)
# cv2.imshow("canny_edge_img.jpg",canny_edge_img)

# cv2.imshow("Input_img", img)
prob_lines = cv2.HoughLinesP(canny_edge_img, 1, np.pi / 180, 150, None, 25, 1)

if prob_lines is not None:
    for i in range(0, len(prob_lines)):
        line = prob_lines[i][0]
        cv2.line(img, (line[0], line[1]), (line[2], line[3]), (0,0,255), 1, cv2.LINE_AA)

n = 0
if '0'<= str[len(str)-5] <= '9':
    n = n + int(str[len(str)-5])

if '0'<= str[len(str)-6] <= '9':
    n = n + 10* int(str[len(str)-6])

cv2.imwrite(f"robolin-tiles{n}.jpg",img)
# cv2.imshow("probabilistic_hough_line_transform_detected", img)
# cv2.waitKey(0)