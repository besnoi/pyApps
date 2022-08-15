'''
    Camera with PySide6 / Neir

    Part of 100 GUI Apps Challenge
    (https://github.com/besnoi/pyApps)

    Challenge Rules :
        1. App must be useful
        2. App must be beautiful
        3. App must be short (<500 LOC)

    And lastly no Plagiarism :D
'''

import sys
from datetime import datetime

from PyQt5.QtMultimedia import QCamera,QCameraInfo
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap, QPainter
import qdarktheme
import requests

class PicButton(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = self.pixmap_hover = self.pixmap_pressed = pixmap
        self.pressed.connect(self.update)
        self.released.connect(self.update)

    def paintEvent(self, event):
        pix = self.pixmap_hover if self.underMouse() else self.pixmap
        if self.isDown():
            pix = self.pixmap_pressed

        painter = QPainter(self)
        painter.drawPixmap(event.rect(), pix)

    def enterEvent(self, event):
        self.update()

    def leaveEvent(self, event):
        self.update()

    def sizeHint(self):
        return QSize(80, 80)


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Camera')
        self.setWindowIcon(QIcon('icon.png'))
        # shutterBtn = QPushButton('Click',self)
        # shutterBtn.setStyleSheet("background: url('icons/capture.png');")
        # shutterBtn.setPixmap()
        shutterBtn=PicButton(QPixmap('icons/capture.png'),self)

        viewImagesBtn = PicButton(QPixmap('icons/images.png'),self)
        recordBtn = PicButton(QPixmap('icons/record.png'),self)
        shutterBtn.setFixedSize(80,80)
        viewImagesBtn.setFixedSize(60,60)
        recordBtn.setFixedSize(60,60)

        self.available_cameras = QCameraInfo.availableCameras()
        if not self.available_cameras:
            quit(-1073740791)

        self.viewfinder = QCameraViewfinder()
        self.viewfinder.show()
        self.camera = QCamera(self.available_cameras[0])
        self.camera.setViewfinder(self.viewfinder)
        self.camera.setCaptureMode(QCamera.CaptureStillImage)
        self.camera.error.connect(lambda: self.alert(self.camera.errorString()))
        self.camera.start()

        layout = QGridLayout() # frame layout
        layout.addWidget(viewImagesBtn, 0, 0, 1, 1, Qt.AlignBottom | Qt.AlignRight)
        layout.addWidget(shutterBtn, 0, 1, 1, 1, Qt.AlignBottom)
        layout.addWidget(recordBtn, 0, 2, 1, 1, Qt.AlignBottom | Qt.AlignLeft)
        self.frame = QWidget()
        self.frame.setLayout(layout)
        # self.setStyleSheet('background:#666')
        # self.frame.setStyleSheet('background:#000;opacity:0.6')
        self.frame.setFixedHeight(100)
        self.frame.setMaximumHeight(50)
        self.viewfinder.setMinimumHeight(150)
        mainLayout = QGridLayout()  # frame layout
        mainLayout.addWidget(self.viewfinder, 0, 0, 2, 3)
        mainLayout.addWidget(self.frame, 1, 0,1,3,Qt.AlignBottom)
        # op = QGraphicsOpacityEffect(self.frame)
        # op.setOpacity(0.60)  # 0 to 1 will cause the fade effect to kick in
        # self.frame.setGraphicsEffect(op)
        # self.setAutoFillBackground(True)
        self.setLayout(mainLayout)

if __name__=='__main__':
    app=QApplication([])
    win=MainWindow()
    win.show()
    app.exec()