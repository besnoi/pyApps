'''
    Sticky Notes with PySide6 / Neir
    
    Part of 100 GUI Apps Challenge
    (https://github.com/besnoi/pyApps)

    Challenge Rules :
        1. App must be useful
        2. App must be beautiful
        3. App must be short (<500 LOC)
    
    And lastly no Plagiarism :D
'''

import sys
from random import choice
from PySide6.QtCore import Qt, QPoint, QRect, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import *

class ImageButton(QToolButton):
    def __init__(self,img,parent=None):
        super().__init__(parent)
        self.setIcon(QIcon(img))
        self.setIconSize(QSize(24,24))
        self.setFixedSize(QSize(24,24))
        self.setStyleSheet('background:transparent;')

NOTE_COLORS=('#fff3ab','#e7cfff','#afe0ec','#c4e2b8')

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sticky Notes")

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setGeometry(QRect(0, 0, 400, 300)) 
        self.center()

        label=QLabel(self.windowTitle())
        label.setFixedHeight(30)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet('background:#555;color:#ccc')
        label.mouseMoveEvent=self.winTopMove
        label.mousePressEvent=self.winTopPress

        addBtn=ImageButton('add.png')
        delBtn=ImageButton('delete.png')
        exitBtn=ImageButton('exit.png')
        exitBtn.clicked.connect(self.close)

        textEdit=QTextEdit('asdfsdf',self)
        textEdit.setStyleSheet(f'background:{choice(NOTE_COLORS)};color:#000;border:none;font-size:18px')

        layout = QGridLayout(self)
        layout.addWidget(label,0,0,1,4)
        layout.addWidget(addBtn,0,0,1,1)
        layout.addWidget(delBtn,0,1,1,1,Qt.AlignLeft)
        layout.addWidget(exitBtn,0,3,1,1)
        layout.addWidget(textEdit,1,0,1,4)
        layout.addWidget(QSizeGrip(self), 1,0,1,1, Qt.AlignBottom | Qt.AlignLeft)
        layout.addWidget(QSizeGrip(self), 1,3,1,1, Qt.AlignBottom | Qt.AlignRight)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.oldPos = self.pos()

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def winTopPress(self, event):
        self.oldPos = event.globalPosition().toPoint() # current mouse pos

    def winTopMove(self, event):
        delta = QPoint (event.globalPosition().toPoint() - self.oldPos) # current mouse pos - last mouse pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition().toPoint()

if __name__=='__main__':
    app = QApplication(sys.argv)
    MainWindow().show()
    sys.exit(app.exec())

