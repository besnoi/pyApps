'''
    FACE COMPARE with PySide6 / Neir
    
    Part of 100 GUI Apps Challenge
    (https://github.com/besnoi/pyApps)

    Challenge Rules :
        1. App must be useful
        2. App must be beautiful
        3. App must be short (<500 LOC)
    
    And lastly no Plagiarism :D
'''

import sys,cv2

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import *

import numpy as np
import urllib
import cv2

def url_to_image(url):
	resp = urllib.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	return image

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Face Compare")


        # button = QPushButton("Press Me!")
        layout = QGridLayout(self)
        self.url1 = QLineEdit()
        url2 = QLineEdit()

        layout.addWidget(QLabel('Enter URL for image1:'),0,0,1,1)
        layout.addWidget(url1,0,1)
        layout.addWidget(QLabel('Enter URL for image2:'),1,0,1,1)
        layout.addWidget(url2,1,1)
        img = QLabel('<img src="https://i.imgur.com/iDUkYEi.png">')
        layout.addWidget(img,2,0,1,1)
        self.url1.enter.activated(self.recognize1)

        self.setLayout(layout)

    def recognize1(self):
        img = url_to_image(self.url1.text())
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detects faces of different sizes in the input image
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            # To draw a rectangle in a face
            cv2.rectangle(img,(x,y),(x+w,y+h),(5,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]

        # Display an image in a window
        cv2.imshow('img',img)


if __name__=='__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())