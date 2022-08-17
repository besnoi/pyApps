'''
    Geolocate IP with PyQt5 / Neir
    
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
from threading import Thread
import sys
import qdarkstyle
import ipinfo
import folium
import io

API_ACCESS_TOKEN = '09d8c3fe6f8ed9' # subject to change

class MainWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('Geolocate IP')

        self.setWindowIcon(QIcon('icon.png'))
        self.handler=ipinfo.getHandler(API_ACCESS_TOKEN)
        self.info = None # domain obj from whois
        self.mapdata = None
        self.timer = QTimer()
        self.process = None # thread

        self.entry = QLineEdit(self)
        self.entry.setPlaceholderText('Enter IP to geolocate: ')

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
        self.webview = QWebEngineView()
        self.layout = None # this will come handy later in addRecord

        self.show()

    # the whois module can sometime give arrays where you don't expect them, hence expectList
    def addRecord(self,i,text,value,expectList=False):
        label = QLabel(text, self)
        label.setMaximumWidth(200)
        self.layout.addWidget(label, i, 0,1,2)
        entry = QLineEdit(str(value), self)
        entry.setReadOnly(True)
        entry.setStyleSheet("border:none")
        self.layout.addWidget(entry, i, 2, 1, 4)
        i += 1
        return i
    def lookup(self):
        # domain obj has not yet been received from the API, so return
        if not self.info or not self.mapdata:
            return
        self.timer.stop()
        # TODO check if there is no internet connection
        if  not self.info.ip:
            return QMessageBox.critical(self,'Error','Invalid IP Address')
        self.layout = QGridLayout()
        frame=QFrame()
        frame.setLayout(self.layout)
        self.layout.addWidget(self.webview, 0,0,1,6)
        self.webview.setHtml(self.mapdata)
        i = 1
        if self.entry.text().strip()=='':
            self.entry.setText(self.info.ip)
        i=self.addRecord(i,'IP:',self.info.ip)
        i=self.addRecord(i,'City:',self.info.city)
        i=self.addRecord(i,'Region:',self.info.region)
        i=self.addRecord(i,'Postal Code:',self.info.postal)
        i=self.addRecord(i,'Country:',self.info.country_name)
        i=self.addRecord(i,'Location:',self.info.loc)
        i=self.addRecord(i,'Organization/ISP:',self.info.org)
        i=self.addRecord(i,'Timezone:',self.info.timezone)
        self.scrollArea.setWidget(frame)
    def getIPInfo(self,ip):
        self.info=self.handler.getDetails(ip)
        m = folium.Map(
        	tiles='Stamen Terrain',
        	zoom_start=10,
        	location=(self.info.latitude, self.info.longitude)
        )

        # save map data to data object
        mapdata = io.BytesIO()
        m.save(mapdata, close_file=False)
        self.mapdata=mapdata.getvalue().decode()

        self.process = None
    def onLookup(self):
        self.info=None
        if self.process: # a thread already running
            return
        url=self.entry.text()
        self.process = Thread(target=self.getIPInfo, args=[url])
        self.process.start()
        self.timer.start(500)
        self.timer.timeout.connect(self.lookup)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    win = MainWindow()
    win.setGeometry(300,300,400,400)
    sys.exit(app.exec_())
