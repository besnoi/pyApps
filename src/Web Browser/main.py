'''
    Web Browser with PyQt5 / Neir
    
    Part of 100 GUI Apps Challenge
    (https://github.com/besnoi/pyApps)

    Challenge Rules :
        1. App must be useful
        2. App must be beautiful
        3. App must be short (<500 LOC)
    
    And lastly no Plagiarism :D
'''

from PyQt5.Qt import *
from PyQt5.QtWebEngineWidgets import *
import sys

HOMESITE = "https://github.com/besnoi"

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Tab - Cyanide Browser")
        self.setWindowIcon(QIcon('browser.ico'))
        self.resize(600, 400)

        self.urlBox = QLineEdit()
        self.urlBox.setMinimumHeight(25)
        cancelBtn = self.urlBox.addAction(QIcon('icons/cancel.png'), self.urlBox.TrailingPosition)
        self.secureBtn = self.urlBox.addAction(QIcon('icons/secure.png'), self.urlBox.LeadingPosition)
        # connect action.triggered signal to a slot


        self.backwardBtn = QAction(QIcon('icons/backward.png'), "Back", self)
        self.forwardBtn = QAction(QIcon('icons/forward.png'), "Forward", self)
        # TODO enable forward backward only when needed
        # self.backwardBtn.setDisabled(True)
        # self.forwardBtn.setDisabled(True)

        self.secureBtn.triggered.connect(lambda: QMessageBox.information(self,'Info','This is a secure page with SSL:', self.urlBox.text()))
        cancelBtn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        self.backwardBtn.triggered.connect(lambda: self.tabs.currentWidget().back())
        self.forwardBtn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        self.urlBox.returnPressed.connect(self.onVisitURL)

        refreshBtn = QAction(QIcon('icons/refresh.png'), "Refresh", self)
        moreBtn = QAction(QIcon('icons/more.png'), "More", self)
        toolBar = self.addToolBar('Navigation')
        toolBar.addAction(self.backwardBtn)
        toolBar.addAction(self.forwardBtn)
        toolBar.setMovable(False)
        toolBar.addAction(refreshBtn)
        toolBar.addWidget(self.urlBox)
        toolBar.addAction(moreBtn)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabBarDoubleClicked.connect(self.onTabDoubleClick)
        self.tabs.tabCloseRequested.connect(lambda i: self.tabs.count()>1 and self.tabs.removeTab(i))
        self.tabs.currentChanged.connect(self.onTabChange)
        self.setCentralWidget(self.tabs)
        self.newTab()

    def newTab(self,url=HOMESITE,title="Loading"):
        page = QWebEngineView()
        if not url:
            url=HOMESITE
        url=QUrl(url)
        page.setUrl(url)
        tabNo = self.tabs.addTab(page,title)
        self.tabs.setCurrentIndex(tabNo)
        page.urlChanged.connect(lambda link,webview=page: self.updateURL(link,webview))
        page.loadFinished.connect(lambda _, i=tabNo, webview=page: self.tabs.setTabText(i, webview.page().title() or 'Loading') and self.updateTitle(webview))
    def onTabDoubleClick(self,i):
        if i==-1:
            self.newTab()
    def onVisitURL(self):
        url = QUrl(self.urlBox.text())
        if url.scheme() == "":
            url.setScheme("http")
        self.tabs.currentWidget().setUrl(url)
    def updateURL(self,url,page=None):
        if page!=self.tabs.currentWidget():
            return
        self.secureBtn.setVisible(url.scheme() == 'https') #SSL
        self.urlBox.setText(url.toString())
        self.urlBox.setCursorPosition(0)
    def updateTitle(self,page):
        if page!=self.tabs.currentWidget():
            return
        title = page.page().title()
        if not title:
            title='New Tab'
        self.setWindowTitle(f'{title} - Cyanide Browser')
    def onTabChange(self):
        self.updateURL(self.tabs.currentWidget().url(),self.tabs.currentWidget())
        self.updateTitle(self.tabs.currentWidget())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
