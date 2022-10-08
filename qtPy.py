import sys

import cv2 as cv
import numpy as np
from PySide6 import QtCore, QtGui, Qt
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QTextEdit


class MainWindow(QMainWindow):
    def __init__(self, img):
        super().__init__()
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
        print((e.x(), e.y()))
        canvas = self.label.pixmap()
        painter = QtGui.QPainter(canvas)
        pen = QtGui.QPen()
        pen.setWidth(3)
        pen.setColor(QtGui.QColor("red"))
        painter.setPen(pen)
        painter.drawRoundedRect(e.x(), e.y(), 10, 10, 100, 100)
        painter.end()
        self.label.setPixmap(canvas)
        return (e.x(), e.y())

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

img = cv.imread('dog.jpg')

window = MainWindow(img)
window.show()

sys.exit(app.exec())