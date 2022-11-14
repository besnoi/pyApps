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

from PySide6.QtGui import QImage,QPixmap
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import *
from facepplib import FacePP
from pathlib import Path
from qtmodern.windows import ModernWindow
from qtmodern.styles import light

import urllib, cv2,imutils,wget,numpy as np

# download trained facedetection xml if not exist
my_file = Path("haarcascade_frontalface_default.xml")
if not my_file.is_file():
    wget.download('https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml')

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def url_to_image(url):
	resp = urllib.request.urlopen(url)
	img = np.asarray(bytearray(resp.read()), dtype="uint8")
	img = cv2.imdecode(img, cv2.IMREAD_COLOR)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)

	for (x,y,w,h) in faces:
		# To draw a rectangle in a face
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,200,0),1)
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = img[y:y+h, x:x+w]
	return img
   
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Face Compare")
        self.setWindowIcon(QPixmap('icon.png'))


        # button = QPushButton("Press Me!")
        layout = QGridLayout(self)
        self.url1 = QLineEdit('https://i.imgur.com/Yydp02V.png')
        self.url2 = QLineEdit('https://i.imgur.com/FZNtGRS.png')
        self.btn = QPushButton('Compare Faces')
        self.btn.setFixedHeight(40)

        layout.addWidget(QLabel('Enter URL for image1:'),0,0,1,1)
        layout.addWidget(self.url1,0,1,1,3)
        layout.addWidget(QLabel('Enter URL for image2:'),1,0,1,1)
        layout.addWidget(self.url2,1,1,1,3)
        self.img1 = QLabel('<img src="https://i.imgur.com/iDUkYEi.png">')
        self.img2 = QLabel('<img src="https://i.imgur.com/iDUkYEi.png">')
        layout.addWidget(self.img1,2,0,1,2)
        layout.addWidget(self.img2,2,2,1,2)
        layout.addWidget(self.btn,3,0,1,4)
        self.url1.returnPressed.connect(self.setImage1)
        self.url2.returnPressed.connect(self.setImage2)
        self.btn.clicked.connect(self.compare)
        self.setImage1()
        self.setImage2()

        self.setLayout(layout)

    def compare(self):

        api_key ='xQLsTmMyqp1L2MIt7M3l0h-cQiy0Dwhl'
        api_secret ='TyBSGw8NBEP9Tbhv_JbQM18mIlorY6-D'
                
        app = FacePP(api_key = api_key, 
                        api_secret = api_secret)
        cmp_ = app.compare.get(image_url1 = self.url1.text(),image_url2 = self.url2.text())

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowIcon(QPixmap('icon.png'))
        msg.setWindowOpacity(0.7)
        # msg.setWindowFlag(Qt.FramelessWindowHint)

        msg.setText(cmp_.confidence>80 and "Both pics are of the same person!!!" or "Pictures do not match!!!")
        msg.setInformativeText(f'Confidence Number : {cmp_.confidence}')
        msg.setWindowTitle("Result")
        msg.setDetailedText("No more details to show")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            
        retval = msg.exec_()
    def setImage1(self):
        image = imutils.resize(url_to_image(self.url1.text()),height=250)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
        self.img1.setPixmap(QPixmap.fromImage(image))

    def setImage2(self):
        image = imutils.resize(url_to_image(self.url2.text()),height=250)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
        self.img2.setPixmap(QPixmap.fromImage(image))
	


if __name__=='__main__':
    app = QApplication(sys.argv)
    light(app)
    win = ModernWindow(MainWindow())
    win.show()
    win.resize(550,430)
    sys.exit(app.exec())