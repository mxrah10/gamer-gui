import sys

import cv2 as cv
import numpy as np
from PySide6 import QtCore, QtGui, Qt
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QTextEdit


class MainWindow(QMainWindow):
    def __init__(self, img):
        super().__init__()
        self.img = img
        self.label = QLabel(self)
        self.pixmap = QPixmap(self.convert_cv_qt(img))
        self.pixmap_resized = self.pixmap.scaled(720, 405, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(self.pixmap_resized)
        self.setCentralWidget(self.label)
        self.setMouseTracking(True)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Mouse Tracker')
        self.resize(self.pixmap.width()/4, self.pixmap.height()/4)

    def mousePressEvent(self, e):
        self.x = e.x()
        self.y = e.y()
        print(self.x, self.y)
        self.setHSV()
        return (e.x(), e.y())

    def setHSV(self):
        colorsB = self.img[self.y, self.x, 0]
        colorsG = self.img[self.y, self.x, 1]
        colorsR = self.img[self.y, self.x, 2]
        hsv_value = np.uint8([[[colorsB, colorsG, colorsR]]])
        self.hsv = cv.cvtColor(hsv_value, cv.COLOR_BGR2HSV)
        print(self.hsv)

    def convert_cv_qt(self, img):
        """Convert from an opencv image to QPixmap"""

        scale_percent = 60  # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

        # resize image
        cv_img = cv.resize(img, dim, interpolation=cv.INTER_AREA)

        height, width, channel = cv_img.shape
        print(cv_img.shape)
        bytesPerLine = 3 * width
        qImg = QImage(cv_img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        return (qImg)

app = QApplication(sys.argv)

img = cv.imread('blitzkrieg.png')

window = MainWindow(img)
window.show()

sys.exit(app.exec())