from read import circleMaker as cm
import cv2 as cv

img = cv.imread('dog2.jpg')
position = (img.shape[1]//2,img.shape[0]//2)
cm.make_dot(img,position)