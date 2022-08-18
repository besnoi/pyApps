import sys, os, io
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt,QBuffer
from PySide6.QtGui import QPixmap
from qtmodern.styles import dark
from qtmodern.windows import ModernWindow
from PIL import Image
class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Drop Image Here \n\n')
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa;
                margin-bottom:10px;
                margin-top:10px;
            }
        ''')

    def setPixmap(self, image):
        super().setPixmap(image)

class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Icon Converter")
        self.setAcceptDrops(True)

        mainLayout = QGridLayout()

        self.photoViewer = ImageLabel()
        self.photoViewer.setFixedSize(256,256)
        mainLayout.addWidget(QLabel('Enter image to convert:'),0,0,1,3)
        browseBtn=QPushButton("Browse")
        convertBtn=QPushButton("Convert")
        resetBtn=QPushButton("Reset")
        closeBtn=QPushButton("Close")
        convertBtn.setStyleSheet("margin-top:10px;height:20px")
        resetBtn.setStyleSheet("margin-top:10px;height:20px")
        closeBtn.setStyleSheet("margin-top:10px;height:20px")

        mainLayout.addWidget(browseBtn,0,4,1,1)
        cb=['16x16','32x32','48x48','64x64','128x128','256x256']
        self.cbArray=[]
        mainLayout.addWidget(self.photoViewer,1,0,1,5,Qt.AlignCenter)
        mainLayout.addWidget(QLabel("Choose Dimensions"),2,0,1,2)
        for i,v in enumerate(cb):
            self.cbArray.append(QCheckBox(v))
            mainLayout.addWidget(self.cbArray[i],2+i//3,2+i%3)
        mainLayout.addWidget(convertBtn,4,0,1,3)
        mainLayout.addWidget(resetBtn,4,3)
        mainLayout.addWidget(closeBtn,4,4)

        browseBtn.clicked.connect(self.openFile)
        convertBtn.clicked.connect(self.convert)
        resetBtn.clicked.connect(self.reset)
        closeBtn.clicked.connect(self.close)

        self.setLayout(mainLayout)
    
    def openFile(self):
        path = QFileDialog.getOpenFileName(self,'Open Image','../','PNG Files (*png);;All Files(*, *)')[0]
        if path:
            self.set_image(path)

    def convert(self):
        pixmap = self.photoViewer.pixmap()
        if not pixmap:
            return QMessageBox.critical(self,'Error','Add an Image First\n')
        try:
            buffer = QBuffer()
            buffer.open(QBuffer.ReadWrite)
            pixmap.save(buffer, "PNG")
            img = Image.open(io.BytesIO(buffer.data()))
            icon_sizes = []
            for cb in self.cbArray:
                if cb.isChecked():
                    icon_sizes.append((eval(cb.text().replace('x',','))))
            path = QFileDialog.getSaveFileName(self, "Save Icon", "../", "Icon Files  (*.ico)")[0]
            if path:
                img.save(path, sizes=icon_sizes)
        except:
            return QMessageBox.critical(self,'Error','Couldn\'t convert the Image to Icon\n')

    def reset(self):
        for cb in self.cbArray:
            cb.setChecked(False)
        # self.photoViewer = ImageLabel()

    def close(self):
        quit()
        

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
        self.photoViewer.setStyleSheet("")
        self.photoViewer.setPixmap(QPixmap(file_path))


if __name__=="__main__":
    app = QApplication(sys.argv)
    #dark(app)
    demo = ModernWindow(AppDemo())
    demo.resize(360,400)
    demo.show()
    sys.exit(app.exec_())
