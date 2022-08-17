import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from qtmodern.styles import dark
from qtmodern.windows import ModernWindow

class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Drop Image Here \n\n')
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa
            }
        ''')

    def setPixmap(self, image):
        super().setPixmap(image)

class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        # self.setWindowTitle("Icon Converter")
        self.resize(360,400)
        self.center()
        self.setAcceptDrops(True)

        mainLayout = QGridLayout()

        self.photoViewer = ImageLabel()
        self.photoViewer.setFixedSize(256,256)
        mainLayout.addWidget(QLabel('Enter image to convert:'),0,0,1,3)
        browseBtn=QPushButton("Browse")
        convertBtn=QPushButton("Convert")
        closeBtn=QPushButton("Close")
        mainLayout.addWidget(browseBtn,0,4,1,1)
        cb0=QCheckBox('16x16')
        cb1=QCheckBox('32x32')
        cb2=QCheckBox('48x48')
        cb3=QCheckBox('64x64')
        cb4=QCheckBox('128x128')
        cb5=QCheckBox('256x256')
        mainLayout.addWidget(self.photoViewer,1,0,1,5,Qt.AlignCenter)
        mainLayout.addWidget(QLabel("Choose Dimensions"),2,0,1,2)
        mainLayout.addWidget(cb0,2,2)
        mainLayout.addWidget(cb1,2,3)
        mainLayout.addWidget(cb2,2,4)
        mainLayout.addWidget(cb3,3,2)
        mainLayout.addWidget(cb4,3,3)
        mainLayout.addWidget(cb5,3,4)
        mainLayout.addWidget(convertBtn,4,0,1,3)
        mainLayout.addWidget(closeBtn,4,3)



        self.setLayout(mainLayout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.set_image(file_path)

            event.accept()
        else:
            event.ignore()

    def set_image(self, file_path):
        self.photoViewer.setPixmap(QPixmap(file_path))

    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

if __name__=="__main__":
    app = QApplication(sys.argv)
    dark(app)
    demo = ModernWindow(AppDemo())
    demo.show()
    sys.exit(app.exec_())
