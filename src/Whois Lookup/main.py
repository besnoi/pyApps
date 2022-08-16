'''
    Whois Domain Lookup with PyQt5 / Neir
    
    Part of 100 GUI Apps Challenge
    (https://github.com/besnoi/pyApps)

    Challenge Rules :
        1. App must be useful
        2. App must be beautiful
        3. App must be short (<500 LOC)
    
    And lastly no Plagiarism :D
'''
from PyQt5.Qt import *

import sys
import qdarkstyle
from threading import Thread
from whois import whois


class MainWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Whois Lookup')

        self.setWindowIcon(QIcon('whois.ico'))
        self.domain = None # domain obj from whois
        self.timer = QTimer()
        self.process = None # thread

        self.entry = QLineEdit(self)
        self.entry.setPlaceholderText('Enter domain name to lookup: ')

        lookup_btn = QPushButton('Lookup',self)
        lookup_btn.setStyleSheet('color:rgb(55,54,59);background-color: rgb(68,138,255);')
        self.entry.setMinimumHeight(25)
        self.entry.setMinimumWidth(225)
        lookup_btn.setMaximumWidth(125)
        lookup_btn.setMinimumHeight(25)
        lookup_btn.clicked.connect(self.onLookup)
        self.entry.returnPressed.connect(self.onLookup)

        layout = QGridLayout()
        self.setLayout(layout)
        layout.addWidget(self.entry, 0,0,1,3)
        layout.addWidget(lookup_btn, 0,3)
        frame = QFrame()
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(frame)
        self.scrollArea.setWidgetResizable(True)
        layout.addWidget(self.scrollArea, 1,0,1,4)
        self.layout = None # this will come handy later in addRecord

        self.show()

    # the whois module can sometime give arrays where you don't expect them, hence expectList
    def addRecord(self,i,text,value,expectList=False):
        label = QLabel(text, self)
        label.setMaximumWidth(200)
        self.layout.addWidget(label, i, 0,1,2)
        if expectList and type(value) is list:
            for v in value:
                entry = QLineEdit(str(v), self)
                entry.setReadOnly(True)
                entry.setStyleSheet("border:none")
                self.layout.addWidget(entry, i, 2, 1, 4)
                i += 1
        else:
            if type(value) is list: # we don't expect a list here
                value=value[0]
            entry = QLineEdit(str(value), self)
            entry.setReadOnly(True)
            entry.setStyleSheet("border:none")
            self.layout.addWidget(entry, i, 2, 1, 4)
            i += 1
        return i
    def lookup(self):
        # domain obj has not yet been received from the API, so return
        if not self.domain:
            return
        self.timer.stop()
        # TODO check if there is no internet connection
        if not self.domain['domain_name']:
            return QMessageBox.critical(self,'Error','Invalid Domain Name')
        self.layout = QGridLayout()
        frame=QFrame()
        frame.setLayout(self.layout)
        i = 0
        dn = self.domain['domain_name']
        i=self.addRecord(i,'Domain Name:',self.domain['domain_name'])
        i=self.addRecord(i,'Registrar:',self.domain['registrar'])
        i=self.addRecord(i,'Organization:',self.domain['org'])
        i=self.addRecord(i,'Creation Date:',self.domain['creation_date'])
        i=self.addRecord(i,'Updated Date:',self.domain['updated_date'])
        i=self.addRecord(i,'Expiration Date:',self.domain['expiration_date'])
        i=self.addRecord(i,'Name Servers:',self.domain['name_servers'],True)
        i=self.addRecord(i,'Whois Server:',self.domain['whois_server'])
        i=self.addRecord(i,'Admin Name:',(self.domain['name'] or 'Unknown'),True)
        if self.domain['address'] and self.domain['city'] and self.domain['registrant_postal_code'] and self.domain['country']:
            i=self.addRecord(i,'Address:',self.domain['address']+','+self.domain['city']+' - '+self.domain['registrant_postal_code']+' ('+self.domain['country']+')')
        i=self.addRecord(i,'Contact:',self.domain['emails'],True)
        self.scrollArea.setWidget(frame)
    def getDomainInfo(self,url):
        self.domain=whois(url)
        self.process = None
    def onLookup(self):
        self.domain=None
        if self.process: # a thread already running
            return
        url=self.entry.text()
        self.process = Thread(target=self.getDomainInfo, args=[url])
        self.process.start()
        self.timer.start(100)
        self.timer.timeout.connect(self.lookup)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    win = MainWindow()
    win.setGeometry(300,300,400,400)
    sys.exit(app.exec_())
