'''
    Dictionary with Tkinter / Neir

    Part of 100 GUI Apps Challenge
    (https://github.com/besnoi/pyApps)

    Challenge Rules :
        1. App must be useful
        2. App must be beautiful
        3. App must be short (<500 LOC)

    And lastly no Plagiarism :D
'''

from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon,QTextCursor
from playsound import playsound
from threading import Thread
import qdarkstyle
import requests

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('English Dictionary')
        self.setWindowIcon(QIcon('icon.png'))
        self.audio = None # audio to play
        self.entry = QLineEdit(self)
        self.entry.setPlaceholderText("Type any word here")
        btn = QPushButton('Search',self)
        btn.setStyleSheet('color:rgb(55,54,59);background-color: rgb(68,138,255);')
        self.entry.setMinimumHeight(28)
        btn.setMinimumHeight(28)
        self.textArea = QTextBrowser(self)
        self.textArea.setAcceptRichText(True)
        layout = QGridLayout()
        layout.addWidget(self.entry,0,0,1,3)
        layout.addWidget(btn,0,3)
        layout.addWidget(self.textArea,1,0,1,4)
        self.frame=QFrame()
        self.frame.setLayout(layout)
        self.setCentralWidget(self.frame)
        self.textArea.anchorClicked.connect(self.playAudio)
        self.entry.returnPressed.connect(self.fetchAPI)
        btn.clicked.connect(self.fetchAPI)

    def fetchAPI(self) -> None:
        self.audio = None # clear audio from prev result
        try:
            response=requests.request("GET", f"https://api.dictionaryapi.dev/api/v2/entries/en/{self.entry.text()}", data={})
            if response.status_code != 200:
                raise Exception('APIError')
            self.setText(response.json()[0])
        except:
            QMessageBox.critical(self,"APIError", "Couldn't connect to the API!")
        

    def setText(self,definitions) -> None:
        self.audio = definitions['phonetics'][0]['audio']
        # TODO make sure that tags (gt/lt) in definitions don't hinder
        self.textArea.setText(f"<span style='font-size:24px'>{definitions['word']}</span><a href='#nothing'><img style='float:right' src='sound.png'></a>")
        self.textArea.append(f"<em>{definitions['phonetics'][-1]['text']}</em><br/>")
        s=""
    
        for word in definitions['meanings']:
            s+=f"<p style='color:lightgrey'>{word['partOfSpeech']}</p>"
            for defn in word['definitions']:
                s+=f"<ul style='list-style-type: none;'><li>{defn['definition']}</li>"+(
                f"<li><em>{defn['example']}</em></li></ul>" if ('example' in defn) else "</ul>")
        self.textArea.append(s)
        self.textArea.moveCursor(QTextCursor.Start)
    
    def playAudio(self) -> None:
        if not self.audio:
            return QMessageBox.critical(self,"Error", "No Audio found for given word!")
        try:
            Thread(target=playsound,args=[self.audio]).start()
        except:
            QMessageBox.critical(self,"Error", "Couldn't play Sound!")


if __name__=='__main__':
    app=QApplication([])
    app.setStyleSheet(qdarkstyle.load_stylesheet('pyside6'))
    win=MainWindow()
    win.show()
    app.exec()