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
from urllib.parse import urlparse,quote,unquote,urljoin

import sys
import time
import bs4
import requests
import pyperclip
import webbrowser
import qdarkstyle

USER_AGENT =  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.68 Safari/537.36"
WORDLIST_PATH = "wordlist.dict"

TEST_TARGET = "https://github.com/besnoi/pyApps/tree/main/src"
TEST_MODE = False

class MainWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Web Crawler')

        self.setWindowIcon(QIcon('crawler.ico'))

        self.path = self.link = ''
        self.urls = []  # list of all crawled urls
        self.iurls = [] # for progress bar
        self.targetURL = ''
        self.depth = 1 # how deep to crawl
        self.curLink = 0
        self.links = -1 # total number of links in particular depth
        self.process = None # Main Thread which we will stop play as our needs
        self.relative = False # crawl only relative urls?
        self.stopThread = False
        self.crawlOver = None # is the scan complete
        self.error = False # to show errors if any
        self.timer = QTimer()

        self.entry = QLineEdit(self)
        self.entry.setPlaceholderText('Enter website to crawl: ')
        label = QLabel('Depth:',self)
        label.setFixedWidth(50)
        self.depthSB = QSpinBox(self)
        self.depthSB.setMinimum(1)
        self.depthSB.setFixedWidth(50)

        crawl_btn = QPushButton('Crawl',self)
        copy_btn = QPushButton('Copy URL',self)
        open_btn = QPushButton('Open URL',self)
        export_btn = QPushButton('Export to File',self)

        self.urlList = QListWidget(self)
        self.urlList.addItems(self.urls)
        self.urlList.doubleClicked.connect(self.openURL)
        crawl_btn.clicked.connect(self.onCrawlURL)
        open_btn.clicked.connect(self.openURL)
        copy_btn.clicked.connect(self.copyURL)
        export_btn.clicked.connect(self.export)

        self.progressBar = QProgressBar(self)
        self.relativeCB = QCheckBox('Only Relative URLs',self)

        open_btn.setStyleSheet('color:rgb(55,54,59);background-color: rgb(68,138,255);')
        self.entry.setMinimumHeight(25)
        crawl_btn.setMaximumWidth(125)
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
        layout.addWidget(self.relativeCB, 1,3)
        layout.addWidget(self.urlList, 2,0,1,4)
        layout.addWidget(self.progressBar, 3,0,1,4)
        layout.addWidget(open_btn, 5,0,1,2)
        layout.addWidget(copy_btn, 5,2)
        layout.addWidget(export_btn, 5,3)

        self.show()
    def openURL(self):
        if len(self.urlList.selectedItems())!=0:
            webbrowser.open(self.urlList.selectedItems()[0].text())
    def closeEvent(self,event):
        # STOP THREAD BEFORE QUITTING
        self.stopThread = True
        time.sleep(0.5)
        quit()
    def copyURL(self):
        if len(self.urlList.selectedItems()) != 0:
            pyperclip.copy(self.urlList.selectedItems()[0].text())
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
        elif self.crawlOver==False:
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
        self.curLink = 0
        self.depth = self.depthSB.value()
        self.targetURL=self.entry.text()
        self.progressBar.setValue(0)
        self.relative = self.relativeCB.isChecked()
        self.crawlOver = False # is the scan over or still running?
        self.urlList.clear()
        self.timer.start(100)
        self.timer.timeout.connect(self.showProgress)
        self.process = Thread(target=self.crawlURL,args=[self.targetURL])
        self.process.start()

    def showProgress(self):
        if self.error:
            self.timer.stop()
            QMessageBox.critical(self, 'Error', self.error)
            self.error = False
            return
        if self.stopThread:
            return self.timer.stop()
        if len(self.iurls) == 0 or self.links==-1:  # no progress to show / total links not calculated yet
            if self.crawlOver:
                self.progressBar.setValue(100)
                self.timer.stop()
            return
        val = int(self.curLink / self.links * 100) # for depth 1 ofc
        # only show progress if it's greater than before
        if self.progressBar.value()<val:
            self.progressBar.setValue(val)
        self.urls += self.iurls
        self.urlList.addItems(self.iurls)
        self.iurls=[] # clear the progress array to make way for next iteration
        if self.crawlOver:
            self.progressBar.setValue(100)
            self.timer.stop()

    # recursive function
    def crawlURLHelper(self,targetURL,depth):
        try:
            response = requests.get(targetURL, headers={"user-agent": USER_AGENT})
            if TEST_MODE:
                print(f"{response} - {targetURL}")
            if response.status_code == 404:
                # if the url you are trying to crawl doesn't exist?
                if depth==0:
                    self.error = "URL doesn't exist"
                    self.process = None
                return
            else:
                # add url to crawllist only if it exists!
                if depth!=0:
                    self.iurls.append(targetURL)
            soup = bs4.BeautifulSoup(response.text,"html.parser")
        except:
            self.error = f"Couldn't connect to {targetURL}"
            self.stopThread = True
            self.process = None
            return
        if depth==self.depth:
            return
        if depth==0:
            self.links=len(soup.find_all('a'))
        for el in soup.find_all('a'):
            if self.stopThread:
                return
            if depth==0:
                self.curLink += 1
            if 'href' not in el.attrs: # not all anchors have href
                continue
            url = el.attrs['href']
            if url.startswith('#') or len(url.strip())==0 or 'mailto:' in url: # #link are not even links
                continue

            # ignore absolute urls if user wants only relative urls
            if self.relative and (':' in url or (len(url)>3 and url[0:2]=='//')):
                continue
            url = urljoin(targetURL,url)
            if url not in self.urls and url not in self.iurls:
                self.crawlURLHelper(url,depth+1)
    def crawlURL(self,targetURL):
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
        self.crawlURLHelper(targetURL,0)
        self.crawlOver = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    w = MainWindow()
    sys.exit(app.exec_())
