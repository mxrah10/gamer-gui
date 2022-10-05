import cv2 as cv
import numpy as np
import sys
#from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
class circleMaker():
    def __init__(self,img):
        self.img = img
    def click_event(self, event, x, y, flags, params):
        if event == cv.EVENT_LBUTTONDOWN:
            self.x = x
            self.y = y
            cv.circle(self.img, (x, y), 10, (0, 0, 255), thickness=-1)
            cv.imshow("image", self.img)
            print(x,y)


if __name__ == "__main__":
    img = cv.imread('dog.jpg', 1)
    temp = circleMaker(img)
    cv.imshow('image', img)
    cv.setMouseCallback('image', temp.click_event)
    cv.waitKey(0)
    cv.destroyAllWindows()



