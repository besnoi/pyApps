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

from itertools import tee
import sys

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon,QTextOption
from PySide6.QtWidgets import *
from qtvscodestyle import load_stylesheet,Theme
from googletrans import Translator

# From Google Translate API
LANGUAGES = {
    'Afrikaans': 'af',
    'Albanian': 'sq',
    'Arabic': 'ar',
    'Azerbaijani': 'az',
    'Basque': 'eu',
    'Bengali': 'bn',
    'Belarusian': 'be',
    'Bulgarian': 'bg',
    'Catalan': 'ca',
    'Chinese Simplified': 'zh-CN',
    'Chinese Traditional': 'zh-TW',
    'Croatian': 'hr',
    'Czech': 'cs',
    'Danish': 'da',
    'Dutch': 'nl',
    'English': 'en',
    'Esperanto': 'eo',
    'Estonian': 'et',
    'Filipino': 'tl',
    'Finnish': 'fi',
    'French': 'fr',
    'Galician': 'gl',
    'Georgian': 'ka',
    'German': 'de',
    'Greek': 'el',
    'Gujarati': 'gu',
    'Haitian Creole': 'ht',
    'Hebrew': 'iw',
    'Hindi': 'hi',
    'Hungarian': 'hu',
    'Icelandic': 'is',
    'Indonesian': 'id',
    'Irish': 'ga',
    'Italian': 'it',
    'Japanese': 'ja',
    'Kannada': 'kn',
    'Korean': 'ko',
    'Latin': 'la',
    'Latvian': 'lv',
    'Lithuanian': 'lt',
    'Macedonian': 'mk',
    'Malay': 'ms',
    'Maltese': 'mt',
    'Norwegian': 'no',
    'Persian': 'fa',
    'Polish': 'pl',
    'Portuguese': 'pt',
    'Romanian': 'ro',
    'Russian': 'ru',
    'Serbian': 'sr',
    'Slovak': 'sk',
    'Slovenian': 'sl',
    'Spanish': 'es',
    'Swahili': 'sw',
    'Swedish': 'sv',
    'Tamil': 'ta',
    'Telugu': 'te',
    'Thai': 'th',
    'Turkish': 'tr',
    'Ukrainian': 'uk',
    'Urdu': 'ur',
    'Vietnamese': 'vi',
    'Welsh': 'cy',
    'Yiddish': 'yi'
}

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Language Translator")
        self.setWindowIcon(QIcon('icon.png'))
        button = QPushButton("Press Me!")

        layout = QGridLayout(self)
        from_=QPlainTextEdit(self)
        to=QPlainTextEdit(self)
        fromCB=QComboBox(self)
        fromCB.addItems(LANGUAGES.keys())

        # set text direction depending on language
        def comboChange(comboBox,textEdit):
            if comboBox.currentText() in ['Arabic','Urdu']:
                textEdit.document().setDefaultTextOption(QTextOption(Qt.AlignRight))
            else:
                textEdit.document().setDefaultTextOption(QTextOption(Qt.AlignLeft))

        toCB=QComboBox(self)
        toCB.addItems(LANGUAGES.keys())

        fromCB.currentIndexChanged.connect(lambda event=None:comboChange(fromCB,from_))
        toCB.currentIndexChanged.connect(lambda event=None:comboChange(toCB,to))
        fromCB.setCurrentText('English')
        toCB.setCurrentText('Urdu')
        swapBtn=QPushButton(self)
        swapBtn.setIcon(QIcon('swap.png'))
        swapBtn.setIconSize(QSize(24,24))
        swapBtn.setStyleSheet('background:none')

        def swap(event=None):
            tmp=toCB.currentIndex()
            toCB.setCurrentIndex(fromCB.currentIndex())
            fromCB.setCurrentIndex(tmp)
            tmp=to.toPlainText()
            to.setPlainText(from_.toPlainText())
            from_.setPlainText(tmp)
        swapBtn.clicked.connect(swap)
        soundBtn=QPushButton()
        soundBtn.setIcon(QIcon('sound.png'))
        soundBtn.setStyleSheet('background:none')
        soundBtn.setIconSize(QSize(24,24))
        def translate(event=None):
            translator=Translator()
            print(from_.toPlainText(),LANGUAGES[fromCB.currentText()],LANGUAGES[toCB.currentText()])
            res=translator.translate(from_.toPlainText(),src=LANGUAGES[fromCB.currentText()],dest=LANGUAGES[toCB.currentText()])
            print(res.text)
            to.setPlainText(res.text)
        translateBtn=QPushButton("Translate")
        translateBtn.setStyleSheet('background:none;border:1px solid lightgray;color:black')
        translateBtn.enterEvent=lambda event=None:translateBtn.setStyleSheet('background:rgb(45,125,154);')
        translateBtn.leaveEvent=lambda event=None:translateBtn.setStyleSheet('background:none;border:1px solid lightgray;color:black')
        translateBtn.clicked.connect(translate)
        layout.addWidget(from_,0,0,1,3)
        layout.addWidget(to,0,3,1,3)
        layout.addWidget(fromCB,1,0,1,3)
        layout.addWidget(toCB,1,3,1,3)
        layout.addWidget(swapBtn,2,0,1,1,Qt.AlignLeft)
        layout.addWidget(translateBtn,2,1,1,4)
        layout.addWidget(soundBtn,2,5,1,1,Qt.AlignRight)

        self.setLayout(layout)


if __name__=='__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet(Theme.QUIET_LIGHT))
    win = MainWindow()
    win.show()
    sys.exit(app.exec())