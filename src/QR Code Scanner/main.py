'''
    QR Code Scanner with PyQt5 & OpenCV / Neir
    
    Part of 100 GUI Apps Challenge
    (https://github.com/besnoi/pyApps)

    Challenge Rules :
        1. App must be useful
        2. App must be beautiful
        3. App must be short (<500 LOC)
    
    And lastly no Plagiarism :D
'''

import sys
from PyQt5.Qt import *
import cv2
import os
import pyperclip
import webbrowser
import qt_material

## special external image processing function from stackxchange (returns link)
def scanQRCode(path):
    image = cv2.imread(path)
    original = image.copy()
    blur = cv2.GaussianBlur(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Morph close
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    # Find contours and filter for QR code
    cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        x, y, w, h = cv2.boundingRect(approx)
        area = cv2.contourArea(c)
        ar = w / float(h)
        if len(approx) == 4 and area > 1000 and (ar > .85 and ar < 1.3):
            cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 3)
            cv2.imwrite('_pycache.png', image)
    return cv2.QRCodeDetector().detectAndDecode(cv2.imread(path))[0]

class MainWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('QR Code Scanner')
        self.setWindowIcon(QIcon('qrcode.ico'))

        self.path = self.link = ''

        label = QLabel('QR Code to Scan: ')
        label.setStyleSheet('color: lightgrey;')
        file_input = QPushButton('Browse')
        open_btn = QPushButton('Open Link')
        reset_btn = QPushButton('Reset')
        copy_btn = QPushButton('Copy')

        file_input.clicked.connect(self.setImage)
        open_btn.clicked.connect(self.openLink)
        reset_btn.clicked.connect(self.reset)
        copy_btn.clicked.connect(self.copyLink)
        open_btn.setStyleSheet('color:rgb(55,54,59);background-color: rgb(68,138,255);')

        self.result = QLabel('')
        self.label = QLabel("<img src='default.png'>")
        self.label.setAlignment(Qt.AlignCenter)
        self.result.setAlignment(Qt.AlignCenter)

        layout = QGridLayout()
        self.setLayout(layout)
        layout.addWidget(label, 0,0)
        layout.addWidget(file_input, 0,3)
        layout.addWidget(self.label, 1,0,1,4)
        layout.addWidget(self.result, 2,0,1,4)
        layout.addWidget(open_btn, 3,0,1,2)
        layout.addWidget(reset_btn, 3,2)
        layout.addWidget(copy_btn, 3,3)

        self.show()

    def closeEvent(self, event):
        # delete the file that we created if it exists
        try:
            os.remove('_pycache.png')
        except OSError:
            pass
        # file.unlink()
        quit()
    def setImage(self):
        self.path = QFileDialog.getOpenFileName(self, "Open QRC Image", ".", "Images(*.jpg *.jpeg *.png)")[0]
        if len(self.path)>5:
            self.link=scanQRCode(self.path)
            self.label.setText(f"<img src='_pycache.png'>")
            self.result.setText(self.link)
            self.result.setStyleSheet('border-radius:25px;background-color:rgb(90,90,90,90);padding:6px')
    def openLink(self):
        if self.link=='':
            QMessageBox.critical(win, "Error!", "No QR-Code found in the image")
        else:
            webbrowser.open(self.link)
    def copyLink(self):
        pyperclip.copy(self.link)
    def reset(self):
        self.path = self.link  = ''
        self.label.setText("<img src='default.png'>")
        self.result.setText('')
        self.result.setStyleSheet('')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    qt_material.apply_stylesheet(app, theme='dark_blue.xml')
    w = MainWindow()
    sys.exit(app.exec_())
