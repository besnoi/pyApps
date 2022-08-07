'''
    URL Fuzzer with PyQt5 / Neir
    
    Part of 100 GUI Apps Challenge
    (https://github.com/besnoi/pyApps)

    Challenge Rules :
        1. App must be useful
        2. App must be beautiful
        3. App must be short (<500 LOC)
    
    And lastly no Plagiarism :D
'''
from PyQt5.Qt import *
from threading import Thread
from urllib.parse import urlparse,quote,unquote

import sys
import time
import requests
import pyperclip
import webbrowser
import qdarkstyle

USER_AGENT =  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.68 Safari/537.36"
WORDLIST_PATH = "wordlist.dict"

TEST_TARGET = "https://github.com/besnoi/pyApps/tree/main"
TEST_MODE = False

class MainWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('URL Fuzzer')

        self.setWindowIcon(QIcon('fuzzer.ico'))

        self.path = self.link = ''
        self.urls = []
        self.iurls = [] # for progress bar
        self.ext = ['php','py','html','txt'] # file extensions to look for
        self.targetURL = ''
        self.makeWordlist()
        self.process = None # Main Thread which we will stop play as our needs
        self.showStatus = False # show status before result
        self.scandir = False # show status before result
        self.stopThread = False
        self.scanOver = None # is the scan complete
        self.error = False # to show errors if any
        self.timer = QTimer()

        self.entry = QLineEdit(self)
        self.entry.setPlaceholderText('Enter website to scan: ')

        fuzz_btn = QPushButton('Scan',self)
        copy_btn = QPushButton('Copy URL',self)
        open_btn = QPushButton('Open URL',self)
        export_btn = QPushButton('Export to File',self)

        self.urlList = QListWidget(self)
        self.urlList.addItems(self.urls)
        self.urlList.doubleClicked.connect(self.openURL)
        fuzz_btn.clicked.connect(self.onScanURL)
        open_btn.clicked.connect(self.openURL)
        copy_btn.clicked.connect(self.copyURL)
        export_btn.clicked.connect(self.export)

        self.progressBar = QProgressBar(self)
        self.status = QCheckBox('Show status',self)
        self.scandirCB = QCheckBox('Scan sub-directories too',self)

        open_btn.setStyleSheet('color:rgb(55,54,59);background-color: rgb(68,138,255);')
        self.entry.setMinimumHeight(25)
        fuzz_btn.setMinimumHeight(25)
        open_btn.setMinimumHeight(25)
        copy_btn.setMinimumHeight(25)
        export_btn.setMinimumHeight(25)

        # TODO USE TABLEVIEW
        layout = QGridLayout()
        self.setLayout(layout)
        layout.addWidget(self.entry, 0,0,1,3)
        layout.addWidget(fuzz_btn, 0,3)
        layout.addWidget(self.scandirCB, 1,0,1,3)
        layout.addWidget(self.status, 1,3)
        layout.addWidget(self.urlList, 2,0,1,4)
        layout.addWidget(self.progressBar, 3,0,1,4)
        layout.addWidget(open_btn, 5,0,1,2)
        layout.addWidget(copy_btn, 5,2)
        layout.addWidget(export_btn, 5,3)

        self.show()

    def getURL(self,url):
        # if there is status "[200] -" etc before url then remove it
        if self.showstatus:
            return url[6:]
        else:
            return url
    def openURL(self):
        if len(self.urlList.selectedItems())!=0:
            webbrowser.open(self.getURL(self.urlList.selectedItems()[0].text()))
    def closeEvent(self,event):
        # STOP THREAD BEFORE QUITTING
        self.stopThread = True
        time.sleep(0.5)
        quit()
    def copyURL(self):
        if len(self.urlList.selectedItems()) != 0:
            pyperclip.copy(self.getURL(self.urlList.selectedItems()[0].text()))
    def export(self):
        if self.scanOver:
            result = ''
            for i in range(self.urlList.count()):
                result+=self.urlList.item(i).text()+'\n'
            path = QFileDialog.getSaveFileName(self, "Save Wordlist", "../", "Text File(*.txt);;ALL(*, *)",
                                               "Text File(*.txt)", )[0]
            try:
                if len(path) > 5:
                    with open(path, 'w') as file:
                        file.write(result)
            except:
                QMessageBox.critical(self, 'Error', "Couldn't export data")
        elif self.scanOver==False:
            QMessageBox.critical(self, 'Error', 'Please wait for scan to complete')
    def makeWordlist(self):
        self.wordlist=[]
        self.lines = 0
        with open(WORDLIST_PATH) as file:
            for i in file.readlines():
                self.lines += 1
                self.wordlist.append(i.rstrip())
    # a precursor to scanURL to set new process and destroy earlier process
    def onScanURL(self):
        if not TEST_MODE and (not self.entry.text() or self.targetURL==self.entry.text()): # null/duplicate requests
            QMessageBox.critical(self, 'Error', 'Duplicate Requests not allowed')
            return
        if self.process and self.curLine != self.lines : # a process already started and still continuing
            self.stopThread = True
            time.sleep(1)
            self.stopThread = False
        self.urls = []  # clear all items
        self.iurls = []
        self.targetURL=self.entry.text()
        self.progressBar.setValue(0)
        self.showStatus = self.status.isChecked()
        self.scandir=self.scandirCB.isChecked()
        self.scanOver = False # is the scan over or still running?
        self.urlList.clear()
        self.timer.start(20)
        self.timer.timeout.connect(self.showProgress)
        self.process = Thread(target=self.scanURL)
        self.process.start()

    def showProgress(self):
        if self.error:
            self.timer.stop()
            QMessageBox.critical(self, 'Error', self.error)
            self.error = False
            return
        if self.stopThread:
            return self.timer.stop()
        if len(self.iurls) == 0:  # no progress to show
            if self.scanOver:
                self.progressBar.setValue(100)
                self.timer.stop()
            return
        val = int(self.curLine / self.lines * 100)
        # only show progress if it's greater than before
        if self.progressBar.value()<val:
            self.progressBar.setValue(val)
        self.urls += self.iurls
        self.urlList.addItems(self.iurls)
        self.iurls=[] # clear the progress array to make way for next iteration
        if self.scanOver:
            self.progressBar.setValue(100)
            self.timer.stop()

    # recursive function
    def scanURLHelper(self,targetURL):
        self.curLine = 0
        for word in self.wordlist:
            self.curLine += 1
            attemptList = [word+'/'] #directory
            if '.' in word:
                attemptList.append(word) #file
            # else: # convert dirnames to extensions
            #     for ext in self.ext:
            #         attemptList.append(f'{word}.{ext}')
            for url in attemptList:
                # stop earlier thread to make way for new thread
                if self.stopThread:
                    return
                try:
                    url = targetURL + quote(url)
                    response = requests.get(url,headers={"user-agent": USER_AGENT})
                    if TEST_MODE:
                        print(f"{response} - {url}")
                    if response.status_code!=404:
                        self.iurls.append(self.showStatus and f"[{response.status_code}] - {unquote(url)}" or unquote(url))
                        if url[-1]=='/': # is a directory and it exists
                            if self.scandir:
                                self.scanURLHelper(url)
                except:
                    self.error = "Couldn't connect to target\nCheck your internet connection"
                    self.process = None
                    return
    def scanURL(self):
        targetURL = self.entry.text()
        if TEST_MODE:
            targetURL = TEST_TARGET
        # add scheme to targetURL if not specified
        try:
            targetURL = urlparse(targetURL)
            if not targetURL.netloc:
                raise
        except:
            self.error = "Invalid URL"
            self.process = None
            return
        scheme = targetURL.scheme
        if not targetURL.scheme:
            scheme="http"
        targetURL=scheme+'://'+targetURL.netloc+targetURL.path
        if targetURL[-1] != '/':
            targetURL += '/'
        # if the url you are trying to brute-force doesn't exist?
        try:
            response = requests.get(targetURL,headers={"user-agent": USER_AGENT})
            if response.status_code==404:
                raise
        except:
            self.error = "URL doesn't exist!"
            self.process = None
            return
        self.scanURLHelper(targetURL)
        self.scanOver = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    w = MainWindow()
    sys.exit(app.exec_())
