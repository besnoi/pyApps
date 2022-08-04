'''
    Notepad with PyQt5 / Neir
    
    Part of 100 GUI Apps Challenge
    (https://github.com/besnoi/pyApps)

    Challenge Rules :
        1. App must be useful
        2. App must be beautiful
        3. App must be short (<500 LOC)
    
    And lastly no Plagiarism :D
'''

from PyQt5.Qt import *
import qdarktheme
import os
windows=[] # to prevent garbage collectors from destroying or window
class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowIcon(QIcon('notepad.ico'))
		self.textArea = QPlainTextEdit()
		self.textArea.setStyleSheet('border:none;font-size:18px')
		self.setCentralWidget(self.textArea)
		self.savePath = ''
		self.updateTitle()

		fileMenu = self.menuBar().addMenu("&File")
		newFileAction = QAction('New',self)
		newWindowAction = QAction('New Window',self)
		openFileAction = QAction('Open...',self)
		saveFileAction = QAction('Save',self)
		saveAsFileAction = QAction('Save As...', self)
		printFileAction = QAction('Print...', self)
		quitAction = QAction('Quit', self)

		newFileAction.triggered.connect(self.newFile)
		newWindowAction.triggered.connect(self.newWindow)
		openFileAction.triggered.connect(self.openFile)
		saveFileAction.triggered.connect(self.saveFile)
		saveAsFileAction.triggered.connect(self.saveAsFile)
		printFileAction.triggered.connect(self.printFile)
		quitAction.triggered.connect(exit)

		fileMenu.addAction(newFileAction)
		fileMenu.addAction(newWindowAction)
		fileMenu.addAction(openFileAction)
		fileMenu.addAction(saveFileAction)
		fileMenu.addAction(saveAsFileAction)
		fileMenu.addAction(printFileAction)
		fileMenu.addAction(quitAction)

		editMenu = self.menuBar().addMenu("&Edit")

		undoAction = QAction('Undo', self)
		redoAction = QAction('Redo', self)
		cutAction = QAction('Cut', self)
		copyAction = QAction('Copy', self)
		pasteAction = QAction('Paste', self)
		selectAllAction = QAction('Select All', self)

		undoAction.triggered.connect(self.textArea.undo)
		redoAction.triggered.connect(self.textArea.redo)
		cutAction.triggered.connect(self.textArea.cut)
		copyAction.triggered.connect(self.textArea.copy)
		pasteAction.triggered.connect(self.textArea.paste)
		selectAllAction.triggered.connect(self.textArea.selectAll)

		editMenu.addAction(undoAction)
		editMenu.addAction(redoAction)
		editMenu.addSeparator()
		editMenu.addAction(cutAction)
		editMenu.addAction(copyAction)
		editMenu.addAction(pasteAction)
		editMenu.addSeparator()
		editMenu.addAction(selectAllAction)

		formatMenu = self.menuBar().addMenu("&Format")
		wordWrapAction = QAction('Word Wrap', self)
		# wordWrapAction.triggered.connect(lambda:self.textArea.setWordWrapMode)
		formatMenu.addAction(wordWrapAction)

		viewMenu = self.menuBar().addMenu("&View")
		lightThemeAction = QAction('Light Theme', self)
		darkThemeAction = QAction('Dark Theme', self)
		lightThemeAction.triggered.connect(lambda:self.setStyleSheet(qdarktheme.load_stylesheet('light')))
		darkThemeAction.triggered.connect(lambda:self.setStyleSheet(qdarktheme.load_stylesheet('dark')))

		viewMenu.addAction(lightThemeAction)
		viewMenu.addAction(darkThemeAction)

		helpMenu = self.menuBar().addMenu("&Help")
		aboutAction = QAction('About...', self)
		# aboutAction.triggered.connect(lambda:QMessageBox.Information(self,'About','Notepad / Neir'))
		helpMenu.addAction(aboutAction)

		self.show()

	def newFile(self):
		self.textArea.setPlainText('')
		self.savePath = ''

	def newWindow(self):
		windows.append(MainWindow())

	def openFile(self):
		path = QFileDialog.getOpenFileName(self,'Open File','../','Text Files (*txt);;All Files(*, *)')[0]
		if path:
			try:
				with open(path) as file:
					self.textArea.setPlainText(file.read())
				self.savePath = path
				self.updateTitle()
			except:
				QMessageBox.critical(self,'Error',"File couldn't be opened")


	def saveAsFile(self):
		path = QFileDialog.getSaveFileName(self, "Save file", "../", "Text documents (*.txt);;All Files (*, *)")[0]

		if path:
			self.savePath=path
			self.updateTitle()
			self.saveFile()

	def saveFile(self):
		if self.savePath:
			try:
				with open(self.savePath,'w') as file:
					file.write(self.textArea.toPlainText())
			except:
				QMessageBox.critical(self, 'Error', "File couldn't be opened")
		else:
			self.saveAsFile()

	def printFile(self):
		dlg = QPrintDialog()
		if dlg.exec_():
			self.textArea.print_(dlg.printer())

	def updateTitle(self):
		self.setWindowTitle(f"{(os.path.basename(self.savePath) if self.savePath else 'Untitled')} - Notepad")

if __name__=='__main__':
	app = QApplication([])
	app.setStyleSheet(qdarktheme.load_stylesheet())
	win = MainWindow()
	app.exec_()
