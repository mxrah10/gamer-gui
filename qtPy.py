import sys

import cv2 as cv
import imutils as imutils
import numpy as np
from PySide6 import QtCore, QtGui, Qt
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QTextEdit


class MainWindow(QMainWindow):
    def __init__(self, img):
        super().__init__()
        self.img = img
        self.label = QLabel(self)
        self.pixmap = QPixmap(self.convert_cv_qt())
        self.label.setPixmap(self.pixmap)
        self.setCentralWidget(self.label)
        self.setMouseTracking(True)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Mouse Tracker')

    def setImage(self, img):
        self.img = img
        self.pixmap = QPixmap(self.convert_cv_qt())
        self.label.setPixmap(self.pixmap)
        self.setCentralWidget(self.label)
        self.update()


    def mousePressEvent(self, e):
        self.x = e.x()
        self.y = e.y()
        print(self.x, self.y)
        self.setHSV()
        self.centroid()
        return (e.x(), e.y())

    def getPoints(self):
        return self.x, self.y
    def setHSV(self):
        colorsB = self.img[self.y, self.x, 0]
        colorsG = self.img[self.y, self.x, 1]
        colorsR = self.img[self.y, self.x, 2]
        hsv_value = np.uint8([[[colorsB, colorsG, colorsR]]])
        self.hsv = cv.cvtColor(hsv_value, cv.COLOR_BGR2HSV)
        colors = self.img[self.y, self.x]
        print("HSV : ", self.hsv)
        print("Red: ", colorsR)
        print("Green: ", colorsG)
        print("Blue: ", colorsB)
        print("BGR Format: ", colors)
        print("Coordinates of pixel: X: ", self.x, "Y: ", self.y)
        print(self.hsv[0][0][0])

    def centroid(self):
        self.maxHSV = np.array([self.hsv[0][0][0] + 10, 255, 255], np.uint8)
        self.minHSV = np.array([self.hsv[0][0][0] - 10, 50, 50], np.uint8)
        hsv_img = cv.cvtColor(self.img, cv.COLOR_BGR2HSV)

        self.frame_threshed = cv.inRange(hsv_img, self.minHSV, self.maxHSV)
        cv.imwrite('output2.jpg', self.frame_threshed)
        cv.imshow("grayscale",self.frame_threshed)
        cnts = cv.findContours(self.frame_threshed.copy(), cv.RETR_EXTERNAL,
                                cv.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        for c in cnts:
            M = cv.moments(c)
            if cv.contourArea(c)>850:
                # calculate x,y coordinate of center
                cX = int((M["m10"] / M["m00"])+0.5)
                cY = int((M["m01"] / M["m00"])+0.5)

                self.x = cX
                self.y = cY
                # put text and highlight the center
                cv.circle(img, (cX, cY), 5, (255, 255, 255), -1)
                cv.putText(img, "centroid", (cX - 25, cY - 25), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                # display the image
                self.setImage(img)
                cv.waitKey(0)

    def convert_cv_qt(self):
        """Convert from an opencv image to QPixmap"""
        self.height, self.width, channel = self.img.shape
        bytesPerLine = 3 * self.width
        qImg = QImage(self.img.data, self.width, self.height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        return (qImg)

app = QApplication(sys.argv)

img = cv.imread('colour_testing.png')
window = MainWindow(img)
window.show()

sys.exit(app.exec())