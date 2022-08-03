# importing required libraries
from PyQt5.Qt import *
import sys
import qdarktheme
from threading import Thread
# from controller import Controller

NUMERIC = list("0123456789")
LOWERCASE = list("abcdefghijklmnopqrstuvwxyz")
UPPERCASE = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
ALPHABETIC = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
ALPHANUMERIC = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
MASTERSET = [NUMERIC,LOWERCASE,UPPERCASE,ALPHABETIC,ALPHANUMERIC]

class MainWindow(QWidget):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.setWindowTitle("Wordlist Generator")
		self.setWindowIcon(QIcon('password.ico'))
		self.queryInput=QLineEdit()
		self.queryInput.setMinimumWidth(240)
		self.queryInput.setPlaceholderText('your query (eg. %dA*A)')
		browseBtn=QPushButton('Browse')
		browseBtn.setFixedWidth(100)
		self.progressBar = QProgressBar()
		self.statusArea = QPlainTextEdit()
		self.statusArea.setReadOnly(True)
		self.varsetCB = QComboBox(self)
		okBtn = QPushButton('OK')
		okBtn.setMinimumHeight(35)
		okBtn.setStyleSheet('background-color: rgb(45,67,90)')
		self.varsetCB.addItems(['012345789','lowercase','UPPERCASE','lowercase + UPPERCASE','Alphanumeric (A-z,0-9)'])
		# statusArea.setPlaceholderText('Status and Other Notifications will appear here')
		self.queryInput.addAction(app.style().standardIcon(QStyle.SP_MessageBoxInformation), self.queryInput.TrailingPosition)
		layout = QFormLayout()
		self.setLayout(layout)
		layout.addRow('Enter Query:',self.queryInput)
		layout.addRow('Variable Set:',self.varsetCB)
		layout.addRow('Save To:',browseBtn)
		layout.addRow(self.statusArea)
		layout.addRow(self.progressBar)
		layout.addRow(okBtn)

		layout.setVerticalSpacing(15)
		layout.setHorizontalSpacing(30)
		layout.setFormAlignment(Qt.AlignLeft | Qt.AlignVCenter)
		okBtn.clicked.connect(self.generateWordlist)
		browseBtn.clicked.connect(self.saveFile)

		self.show()

	def generateWordlist(self):
		self.arr = []  # a[i]=[set=[],pos=[],cur=i)
		self.query = self.queryInput.text().strip()  # query for our wordlist
		self.noc = 0  # number of combinations so far (for progress bar)
		self.tnoc = 1  # total number of combinations needed
		self.offset = 0  # we need this for inputs with bracket []
		self.varset = self.varset = MASTERSET[self.varsetCB.currentIndex()]  # identifier set
		self.result = ''  # result to print/write to file
		self.iresult = ''  # result for last increment (for showing progress)
		self.statusArea.setPlainText('')
		self.parseInput()
		self.timer = QTimer()
		self.timer.start(20)
		self.timer.timeout.connect(self.showProgress)
		process = Thread(target=self.runLoop, args=[0])
		process.start()
	
	def showProgress(self):
		self.progressBar.setValue(int(self.noc / self.tnoc * 100))
		if self.iresult=='': # no progress to show
			return
		self.result += self.iresult
		self.statusArea.appendPlainText(self.iresult)
		self.iresult = ''
		if (self.noc == self.tnoc):
			self.timer.stop()

	def saveFile(self):
		if self.result=='':
			return QMessageBox.critical(self, 'Error!', 'Enter Query First!')
		try:
			path = QFileDialog.getSaveFileName(self, "Save Wordlist", "../", "Text File(*.txt);;ALL(*, *)","Text File(*.txt)", )[0]
			if len(path)>5:
				with open(path,'w') as file:
					file.write(self.result)
		except IOError:
			QMessageBox.critical("Error!", "File couldn't be saved!")

	def parseInput(self):
		visited = {}
		i = 0
		while i<len(self.query):
			# self.statusArea.appendPlainText(self.query[i])
			if self.query[i] == '#':
				self.arr.append([NUMERIC, [i - self.offset], 0])
				self.tnoc *= len(NUMERIC)
			elif self.query[i] == '$':
				self.arr.append([UPPERCASE, [i - self.offset], 0])
				self.tnoc *= len(UPPERCASE)
			elif self.query[i] == '%':
				self.arr.append([LOWERCASE, [i - self.offset], 0])
				self.tnoc *= len(LOWERCASE)
			elif self.query[i] == '*':
				self.arr.append([ALPHABETIC, [i - self.offset], 0])
				self.tnoc *= len(ALPHABETIC)
			elif self.query[i] == '^':
				self.arr.append([ALPHANUMERIC, [i - self.offset], 0])
				self.tnoc *= len(ALPHANUMERIC)
			elif 65 <= ord(self.query[i]) <= 90:
				# if identifier then set position value to array
				t, j = [i - self.offset], i + 1
				if not self.query[i] in visited:
					visited[self.query[i]] = True
					offset2 = 0 # to handle pos for A[asdf]A
					while j < len(self.query):
						if self.query[j] == self.query[i]:
							t.append(j - self.offset - offset2)
						elif self.query[j]=='[':
							j = j + 1
							while j < len(self.query):
								offset2 +=1
								if self.query[j]==']':
									break
								j += 1
						j = j + 1
					self.arr.append([self.varset, t, 0])
					self.tnoc*=len(self.varset)
			elif self.query[i] == '[':
				t, j = [], i + 1
				while j < len(self.query):
					if self.query[j] == ']':
						break
					t.append(self.query[j])
					j = j + 1
				self.arr.append([t, [i - self.offset], 0])
				self.tnoc *= len(t)
				self.offset = self.offset + j - i
				i = j
			else:
				self.arr.append([[self.query[i]], [i - self.offset], 0])
			i = i + 1

	def runLoop(self, i):
		if i == len(self.arr):
			self.printCombination()
		else:
			self.arr[i][2] = 0
			while self.arr[i][2] < len(self.arr[i][0]):
				self.runLoop(i + 1)
				self.arr[i][2] += 1

	# TODO - need to refactor this code to improve speed
	def printCombination(self):
		self.noc += 1
		str = list('-' * (len(self.query) - self.offset))
		for i in self.arr:
			j = 0
			while j < len(i[1]):
				str[i[1][j]] = i[0][i[2]]
				j += 1
		s = ""
		for i in str:
			s = s + i
		self.iresult+=s+'\n'
		print(s)

if __name__=='__main__':
	app = QApplication(sys.argv)
	app.setStyleSheet(qdarktheme.load_stylesheet())
	window = MainWindow()
	sys.exit(app.exec_())
