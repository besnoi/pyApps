'''
    Language Translator with PySide6 / Neir
    
    Part of 100 GUI Apps Challenge
    (https://github.com/besnoi/pyApps)

    Challenge Rules :
        1. App must be useful
        2. App must be beautiful
        3. App must be short (<500 LOC)
    
    And lastly no Plagiarism :D
'''

import sys

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import *


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        button = QPushButton("Press Me!")

        layout = QGridLayout(self)
        from_=QPlainTextEdit(self)
        to=QPlainTextEdit(self)
        fromCB=QComboBox(self)
        toCB=QComboBox(self)
        # swap=QPushButton(self)
        layout.addWidget(from_,0,0,1,3)
        layout.addWidget(to,0,4,1,3)
        layout.addWidget(fromCB,1,0,1,3)
        layout.addWidget(toCB,1,4,1,3)
        # layout.addWidget(swap,1,3,1,1)

        self.setLayout(layout)


if __name__=='__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())