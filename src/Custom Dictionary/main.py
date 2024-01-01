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
import qdarkstyle
import requests

import sqlite3

class Dictionary:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("dictionary.db")
        self.cursor = self.conn.cursor()
    
    def getWordList(self,word) -> list:
        word = word.lower().strip()
        return self.cursor.execute(f"SELECT * FROM 'definitions' WHERE word='{word}'").fetchone()
    
    def exists(self,word) -> bool:
        word = word.lower().strip()
        return self.cursor.execute(f"SELECT word FROM 'definitions' WHERE word='{word}'").fetchone();

    def updateRecord(self,word,defn,eg1,eg2) -> None:
        word = word.lower().strip()
        self.cursor.execute(f"UPDATE 'definitions' SET definition='{defn}',example_src='{eg1}',example_dest='{eg2}' WHERE word='{word}'");
        self.conn.commit()

    def writeRecord(self,word,defn,eg1,eg2) -> None:
        word = word.lower().strip()
        self.cursor.execute(f"INSERT INTO 'definitions' VALUES('{word}','{defn}','{eg1}','{eg2}')");
        self.conn.commit()
    
dictionary = Dictionary()

     
class EditDialog(QDialog):

    def __init__(self, parent,word=None, definition=None, example1=None, example2=None):
        super(EditDialog, self).__init__(parent)
        # Create widgets
        self._parent=parent
        self.word = QLineEdit(word or "Word")
        self.definition = QLineEdit(definition or "Definition")
        self.example1 = QLineEdit(example1 or "Example")
        self.example2 = QLineEdit(example2 or "Translation of Example")
        self.button = QPushButton("OK")
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.word)
        layout.addWidget(self.definition)
        layout.addWidget(self.example1)
        layout.addWidget(self.example2)
        layout.addWidget(self.button)
        self.setWindowTitle("Edit a definition")
        # Set dialog layout
        self.setLayout(layout)

        self.button.clicked.connect(self.updateData)

    def updateData(self):
        if dictionary.exists(self.word.text()):
            dictionary.updateRecord(self.word.text(),self.definition.text(),self.example1.text(),self.example2.text())
        else:
            dictionary.writeRecord(self.word.text(),self.definition.text(),self.example1.text(),self.example2.text())
        self._parent.fetchAPI()
        self.close()



class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Custom Dictionary')
        self.setWindowIcon(QIcon('icon.png'))
        
        self.rows =[] # to store result
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
        self.textArea.anchorClicked.connect(self.editWord)
        self.entry.returnPressed.connect(self.fetchAPI)
        btn.clicked.connect(self.fetchAPI)

    def fetchAPI(self) -> None:
        self.rows=dictionary.getWordList(self.entry.text())
        if self.rows:
            self.setText(self.rows)
        else:
            self.textArea.setText("<a href='#nothing'><img style='float:right' src='add.png'></a><br> <em> No Definition Found</em>")

    def setText(self,definition) -> None:
        # TODO make sure that tags (gt/lt) in definitions don't hinder
        self.textArea.setText(f"<span style='font-size:24px;'>{definition[1]} ({definition[0].capitalize()})</span><a href='#nothing'><img style='float:right' src='edit.png'></a>")
        self.textArea.append(f"<br/>Example : <ul style='list-style-type: none;'><li>{definition[2]}</li><li>{definition[3]}</li>")
        self.textArea.moveCursor(QTextCursor.Start)
    
    def editWord(self) -> None:
        if self.rows:
            EditDialog(self,self.rows[0],self.rows[1],self.rows[2],self.rows[3]).show()
        else:
            EditDialog(self,self.entry.text()).show()


if __name__=='__main__':
    app=QApplication([])
    app.setStyleSheet(qdarkstyle.load_stylesheet('pyside6'))
    win=MainWindow()
    win.show()
    app.exec()