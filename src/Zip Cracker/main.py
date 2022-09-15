'''
    Zip Cracker with PyQt5 / Neir
    
    Part of 100 GUI Apps Challenge
    (https://github.com/besnoi/pyApps)

    Challenge Rules :
        1. App must be useful
        2. App must be beautiful
        3. App must be short (<500 LOC)
    
    And lastly no Plagiarism :D
'''

from PyQt5.Qt import *
import zipfile,qt_material,sys
from threading import Thread

WORDLIST_FILE = 'wordlist.txt'

class MainWindow(QWidget):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.setWindowTitle("Zip Cracker")
		self.setWindowIcon(QIcon('icon.png'))
		self.zipFile='protected.zip'
		self.pwdFound=False
		self.error = None # error while extracting zip?
		self.path=QLineEdit(self.zipFile)
		self.wordlist = list(open(WORDLIST_FILE, 'r'))
		browseBtn=QPushButton('Browse')
		browseBtn.setFixedWidth(100)
		self.progressBar = QProgressBar()
		self.statusArea = QTextEdit()
		self.statusArea.setReadOnly(True)
		self.statusArea.setMinimumWidth(400)
		okBtn = QPushButton('Crack Zip File')
		okBtn.setMinimumHeight(35)
		browseBtn.setFixedHeight(35)
		okBtn.setStyleSheet('background-color: rgb(45,67,90)')
		# statusArea.setPlaceholderText('Status and Other Notifications will appear here')
		layout = QGridLayout()
		self.setLayout(layout)
		layout.addWidget(self.path,0,0,1,1)
		layout.addWidget(browseBtn,0,1,1,1)
		layout.addWidget(self.statusArea,1,0,1,2)
		layout.addWidget(self.progressBar,2,0,1,2)
		layout.addWidget(okBtn,3,0,1,2)

		layout.setVerticalSpacing(15)
		layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
		okBtn.clicked.connect(self.crackZipFile)
		browseBtn.clicked.connect(self.openZipFile)

	def crackZipFile(self):
		self.statusArea.setPlainText('')
		self.totalWords = len(self.wordlist)
		print(self.totalWords)
		self.curWord = 0
		process = Thread(target=self.crack)
		process.start()
		self.timer = QTimer()
		self.timer.start(100)
		self.timer.timeout.connect(self.showProgress)
		
	def crack(self):
		zip=zipfile.ZipFile(self.zipFile)
		for word in self.wordlist:
			self.curWord+=1
			try:
				if word.strip()=='idontknow':
					print('found')
				zip.extractall(pwd=bytes(word.strip(), 'utf-8'))
				print('found')
			except RuntimeError: # bad password
				continue
			except Exception as e: # some other error?
				self.error=e
			else:
				self.pwdFound=word
				print("[+] Password found:", word.decode().strip())
				break

	
	def showProgress(self):
		# print('progressing',self.curWord,self.totalWords)
		if self.curWord == self.totalWords:
			self.statusArea.append('<span style="color:red">Password not Found!</span>\n')
			self.timer.stop()
			self.statusArea.append(f'Number of words searched: {self.curWord}/{self.totalWords}\n')
		elif self.pwdFound:
			self.statusArea.append(f'<span style="color:green">Password Found: {self.pwdFound}</span>\n')
			self.timer.stop()
			self.pwdFound=False
			self.statusArea.append(f'Number of words searched: {self.curWord}/{self.totalWords}\n')
			return
		self.progressBar.setValue(int(self.curWord / self.totalWords * 100))
		
			
		


	def openZipFile(self):
		try:
			path = QFileDialog.getOpenFileName(self, "Open Zip File", "../", "Zip Files(*.zip);;ALL(*, *)","Zip Files(*.zip)", )[0]
			if len(path)>5:
				self.zipFile=path
				self.path.setText(path)
				
		except IOError:
			QMessageBox.critical("Error!", "File couldn't be opened!")



if __name__=='__main__':
	app = QApplication(sys.argv)
	qt_material.apply_stylesheet(app, theme='dark_cyan.xml')
	window = MainWindow()
	window.show()
	sys.exit(app.exec_())
