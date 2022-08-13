'''
    Urban Dictionary with Tkinter / Neir

    Part of 100 GUI Apps Challenge
    (https://github.com/besnoi/pyApps)

    Challenge Rules :
        1. App must be useful
        2. App must be beautiful
        3. App must be short (<500 LOC)

    And lastly no Plagiarism :D
'''

from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon
import qdarkstyle
import requests

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Urban Dictionary')
        self.setWindowIcon(QIcon('icon.png'))
        self.entry = QLineEdit(self)
        self.entry.setPlaceholderText("Type any word here")
        btn = QPushButton('Search',self)
        btn.setStyleSheet('color:rgb(55,54,59);background-color: rgb(68,138,255);')
        self.entry.setMinimumHeight(28)
        btn.setMinimumHeight(28)
        self.textArea = QTextEdit(self)
        self.textArea.setReadOnly(True)
        layout = QGridLayout()
        layout.addWidget(self.entry,0,0,1,3)
        layout.addWidget(btn,0,3)
        layout.addWidget(self.textArea,1,0,1,4)
        self.frame=QFrame()
        self.frame.setLayout(layout)
        self.setCentralWidget(self.frame)
        self.entry.returnPressed.connect(self.fetchAPI)
        btn.clicked.connect(self.fetchAPI)

    def fetchAPI(self) -> None:
        try:
            response=requests.request("GET", f"https://api.urbandictionary.com/v0/define?term={self.entry.text()}", data={})
            if response.status_code != 200:
                raise Exception('APIError')
            self.setText(response.json()['list'])
        except:
            QMessageBox.critical(self,"APIError", "Couldn't connect to the API!")

    def setText(self,definitions) -> None:
        # TODO make sure that tags (gt/lt) in definitions don't hinder
        self.textArea.setText(f"<h1>{definitions[0]['word']}</h1>")
        for word in definitions:
            self.textArea.append(
                f"<span>{word['definition']}<br/>"
                f"<em>{word['example']}</em></span>"
            )


if __name__=='__main__':
    app=QApplication([])
    app.setStyleSheet(qdarkstyle.load_stylesheet('pyside6'))
    win=MainWindow()
    win.show()
    app.exec()
