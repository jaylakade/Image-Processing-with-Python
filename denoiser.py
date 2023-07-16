import cv2 
import numpy as np
import pandas as pd
import sys

# 2:16 winsize = 3


def distance(x1,y1,x2,y2):
    dist = np.abs((x1-x2)**2-(y1-y2)**2)
    return np.sqrt(dist)

def gaussian_fun(x,sigma):
    const_val = np.divide(1.0,(2*np.pi*(sigma**2)))
    func_val = np.exp(-(x**2)/(2*(sigma**2)))
    return const_val*func_val

def get_bilateral_filter(noisy_img,win_size,sigma_s,sigma_r):
    height,length,channel = noisy_img.shape
    denoised_img = np.zeros((height,length,channel))

    for ch in range(channel):
        ch_img = np.zeros((height,length))
        for i in range(int(min(height,400))):
            print(i)
            for j in range(min(length,400)):
                weight_wp = 0
                Bifiltered_img_px = 0
                window_size=3
                for k in range(window_size):
                    for l in range(window_size):
                        x = 0
                        y = 0
                        if (i - (window_size/2 - k)) >= height:
                            x = int(i - (window_size/2 - k) - height)
                        else :
                            x = int(i - (window_size/2 - k))
                        
                        if (j - (window_size/2 - l)) >= length:
                            y = int(j - (window_size/2 - l) - length)
                        else :
                            y = int(j - (window_size/2 - l))

                        gs = gaussian_fun(distance(x,y,i,j), sigma_s)
                        p_q = int(noisy_img[x][y][ch]) - int(noisy_img[i][j][ch])
                        gi = gaussian_fun(p_q, sigma_r)
                        Bifiltered_img_px = (Bifiltered_img_px) + (noisy_img[x][y][ch] * gi*gs)
                        weight_wp += gi*gs

                Bifiltered_img_px = Bifiltered_img_px // weight_wp
                # print(Bifiltered_img_px)
                ch_img[i][j] = int(Bifiltered_img_px)
                denoised_img[i][j][ch] = ch_img[i][j]
        # print(ch)
    denoised_img = cv2.bilateralFilter(noisy_img,win_size,sigma_r,sigma_s)
    return denoised_img

str = str(sys.argv[1])
input_img = cv2.imread(str)

# input_img = cv2.imread('noisy1.jpg')
print(input_img.shape)

if(str == "noisy1.jpg"):
    sigma_s = 60
    sigma_r = 120
    window_size = 17
elif(str == "noisy2.jpg"):
    sigma_s = 40
    sigma_r = 60
    window_size = 9
else:
    sigma_s = 50
    sigma_r = 90
    window_size = 13

denoised_img = get_bilateral_filter(input_img,window_size,sigma_s,sigma_r)
print(denoised_img.shape)

cv2.imwrite('denoised.jpg',denoised_img)