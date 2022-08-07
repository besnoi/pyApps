'''
    Web Crawler with PyQt5 & BeautifulSoup / Neir
    
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
        self.setWindowTitle('Web Crawler')

        self.setWindowIcon(QIcon('crawler.ico'))

        self.path = self.link = ''
        self.urls = []
        self.iurls = [] # for progress bar
        self.targetURL = ''
        self.curDepth = 0
        self.process = None # Main Thread which we will stop play as our needs
        self.showStatus = False # show status before result
        self.stopThread = False
        self.crawlOver = None # is the scan complete
        self.error = False # to show errors if any
        self.timer = QTimer()

        self.entry = QLineEdit(self)
        self.entry.setPlaceholderText('Enter website to crawl: ')
        label = QLabel('Depth:',self)
        label.setFixedWidth(50)
        self.depthSB = QSpinBox(self)
        self.depthSB.setFixedWidth(50)

        crawl_btn = QPushButton('Crawl',self)
        copy_btn = QPushButton('Copy URL',self)
        open_btn = QPushButton('Open URL',self)
        export_btn = QPushButton('Export to File',self)

        self.urlList = QListWidget(self)
        self.urlList.addItems(self.urls)
        self.urlList.doubleClicked.connect(self.openURL)
        crawl_btn.clicked.connect(self.onScanURL)
        open_btn.clicked.connect(self.openURL)
        copy_btn.clicked.connect(self.copyURL)
        export_btn.clicked.connect(self.export)

        self.progressBar = QProgressBar(self)
        self.status = QCheckBox('Show status',self)

        open_btn.setStyleSheet('color:rgb(55,54,59);background-color: rgb(68,138,255);')
        self.entry.setMinimumHeight(25)
        crawl_btn.setMaximumWidth(100)
        crawl_btn.setMinimumHeight(25)
        open_btn.setMinimumHeight(25)
        copy_btn.setMinimumHeight(25)
        export_btn.setMinimumHeight(25)

        layout = QGridLayout()
        self.setLayout(layout)
        layout.addWidget(self.entry, 0,0,1,3)
        layout.addWidget(crawl_btn, 0,3)
        layout.addWidget(label, 1,0)
        layout.addWidget(self.depthSB, 1,1,1,2)
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
        if self.crawlOver:
            result = ''
            for i in range(self.urlList.count()):
                result+=self.urlList.item(i).text()+'\n'
            path = QFileDialog.getSaveFileName(self, "Export Results", "../", "Text File(*.txt);;ALL(*, *)",
                                               "Text File(*.txt)", )[0]
            try:
                if len(path) > 5:
                    with open(path, 'w') as file:
                        file.write(result)
            except:
                QMessageBox.critical(self, 'Error', "Couldn't export data")
        elif self.scanOver==False:
            QMessageBox.critical(self, 'Error', 'Please wait for scan to complete')
    # a precursor to scanURL to set new process and destroy earlier process
    def onCrawlURL(self):
        if not TEST_MODE and (not self.entry.text() or self.targetURL==self.entry.text()): # null/duplicate requests
            QMessageBox.critical(self, 'Error', 'Duplicate Requests not allowed')
            return
        if self.process and not self.crawlOver : # a process already started and still continuing
            self.stopThread = True
            time.sleep(1)
            self.stopThread = False
        self.urls = []  # clear all items
        self.iurls = []
        self.depth = self.depthSB.value()
        self.targetURL=self.entry.text()
        self.progressBar.setValue(0)
        self.showStatus = self.status.isChecked()
        self.crawlOver = False # is the scan over or still running?
        self.urlList.clear()
        self.timer.start(20)
        self.timer.timeout.connect(self.showProgress)
        self.process = Thread(target=self.crawlURL,args=[self.targetURL,0])
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
    def crawlURL(self,targetURL,depth):
        self.curDepth = depth
        if self.curDepth==self.depth:
            return

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    w = MainWindow()
    sys.exit(app.exec_())
