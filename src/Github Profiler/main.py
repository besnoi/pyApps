'''
    Github Profiler with PySide6 / Neir
    
    Part of 100 GUI Apps Challenge
    (https://github.com/besnoi/pyApps)

    Challenge Rules :
        1. App must be useful
        2. App must be beautiful
        3. App must be short (<500 LOC)
    
    And lastly no Plagiarism :D
'''

import sys
from datetime import datetime

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import QIcon,QPixmap
import qdarktheme
import requests
from pyqtgraph import mkPen,PlotWidget as QPlotWidget
from io import BytesIO
from PIL import Image,ImageQt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Github Profiler')
        self.setWindowIcon(QIcon('github.ico'))
        self.weeks = [] # for plotting
        self.pen=mkPen(color=(85, 200, 85))
        self.curYear = datetime.now().year # current year

        self.username = QLineEdit(self)

        self.userpic = QLabel(self)
        self.userpic.setVisible(False)
        self.userpic.setMaximumWidth(150)
        self.userpic.setMaximumHeight(150) # height can be dynamic depending on self.labels
        self.year = QSpinBox(self)
        self.year.setMinimum(2008)
        self.year.setMaximum(self.curYear)
        self.year.setValue(self.curYear)
        self.year.setStyleSheet("margin:5px")
        self.username.setMinimumWidth(200)
        self.year.setFixedWidth(70)
        self.username.setPlaceholderText('Enter your username:')
        plotBtn=QPushButton('Plot',self)
        # plotBtn.setMinimumSize(100,55)
        plotBtn.setStyleSheet('color:rgb(55,54,59);background-color: rgb(68,138,200);')

        self.labels=[]
        self.labels.append(QLabel('Name: ',self))
        self.labels.append(QLabel('Location: ',self))
        self.labels.append(QLabel('Public Repos: ',self))
        self.labels.append(QLabel('Public Gists: ',self))
        self.labels.append(QLabel('Max Commits a day (2019): ',self)) # we will change this
        self.labels.append(QLabel('Min Commits a day (2019): ',self)) # we will change this
        self.labels.append(QLabel('Followers: ',self))

        # above were simple self.labels we had nothing to do with once inited
        # but these ones are where we will output
        self.values=[QLabel('Some value',self) for i in self.labels]
        self.userInfo = ['' for i in self.labels] # for putting user information

        self.graphWidget = QPlotWidget(self)
        self.graphWidget.setBackground('#323232')
        self.graphWidget.setLabel('left', 'Contributions')
        self.graphWidget.setLabel('bottom', 'Weeks<span style="font-size:2px"><br/></span>')

        layout = QGridLayout()
        layout.addWidget(self.username, 0, 0, 1, 3)
        layout.addWidget(plotBtn, 0, 3, 1, 1)
        layout.addWidget(self.userpic, 1, 0, len(self.labels), 1)
        i = 0
        while i < len(self.labels):
            self.labels[i].setMinimumWidth(200)
            self.labels[i].setVisible(False)
            self.values[i].setVisible(False)
            layout.addWidget(self.labels[i], 1+i, 1, 1, 1,Qt.AlignLeft)
            layout.addWidget(self.values[i], 1+i, 2, 1, 2,Qt.AlignLeft)
            i+=1
        layout.addWidget(self.graphWidget, 2+i, 0, 1, 4)
        layout.addWidget(self.year, 2+i, 3,Qt.AlignTop)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        # plot default values
        # self.graphWidget.plot([1, 2, 3, 4], [10,50,20,70],symbol ='o', symbolPen ='w', symbolBrush = 0.2)

        plotBtn.clicked.connect(self.setProfile)
        # self.username.returnPressed.connect(self.year.setFocus)
        self.username.returnPressed.connect(self.setProfile)

    def getSkylineAPIResponse(self):
        try:
            response = requests.request("GET", f'https://skyline.github.com/{self.username.text()}/{self.year.value()}.json')
            if response.status_code != 200:
                raise
            response = response.json()
            if not response['contributions']:
                raise TypeError
            self.weeks=[]
            self.userInfo[4]=response['max']
            self.userInfo[5]=response['min']
            for week in response['contributions']:
                sum=0
                for day in week['days']:
                    sum+=day['count']
                self.weeks.append(sum)
        except TypeError:
            QMessageBox.critical(self,'Error',"Wrong username or year")
            return True
        except:
            QMessageBox.critical(self,'Error',"Couldn't connect to Skyline API")
            return True

    def plot(self):
        self.graphWidget.clear()
        self.getSkylineAPIResponse()
        try:
            self.graphWidget.setTitle(f'{self.username.text().capitalize()}\'s Report Card - 2019')
            self.graphWidget.plot([i+1 for i in range(len(self.weeks))], self.weeks,pen=self.pen)
        except:
            QMessageBox.critical(self,'Error',"Couldn't plot the graph\nPls Contact Neir!")
            return True

    def setProfile(self):
        try:
            response = requests.request("GET", f'https://api.github.com/users/{self.username.text()}')
            if response.status_code != 200:
                raise
            response = response.json()
            self.userInfo[0]=response['name']
            self.userInfo[1]=response['location']
            self.userInfo[2]=response['public_repos']
            self.userInfo[3]=response['public_gists']
            self.userInfo[6]=response['followers']
            self.userInfo.append(str(response['avatar_url']))
        except:
            QMessageBox.critical(self,'Error',"Couldn't connect to Users API")
        try:
            response = requests.get(response['avatar_url'])
            self.userpic.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(Image.open(BytesIO(response.content)))).scaledToWidth(150))
        except:
            QMessageBox.critical(self,'Error',"Couldn't set User Avatar")
        self.plot()
        i = 0
        self.labels[4].setText(f'Max Commits a day ({self.year.value()})')
        self.labels[5].setText(f'Min Commits a day ({self.year.value()})')
        while i < len(self.values):
            self.values[i].setText(str(self.userInfo[i]))
            self.values[i].setVisible(True)
            self.labels[i].setVisible(True)
            i += 1
        self.userpic.setVisible(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet())
    main = MainWindow()
    main.setMinimumSize(400,400)
    main.show()
    app.exec()
