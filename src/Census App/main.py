'''
    CENSUS APP with PySide6 / Neir
    
    Part of 100 GUI Apps Challenge
    (https://github.com/besnoi/pyApps)

    Challenge Rules :
        1. App must be useful
        2. App must be beautiful
        3. App must be short (<500 LOC)
    
    And lastly no Plagiarism :D
'''

import sys
from typing import Sequence

from census import Census
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import *
from PySide6.QtGui import QColor,QPainter,QPen,QFont,QIcon
from PySide6.QtCharts import *
from qtmodern.styles import dark
from qtmodern.windows import ModernWindow

census=Census()
states = census.getStateList()
districts = census.getDistrictList()
# TODO check if district name is same
# states=['Arunachal Pradesh','Assam','Bihar','Goa','Kerala','Manipur','Meghalaya','Mizoram','West Bengal']
uts=['Jammu & Kashmir','Delhi','Ladakh','Puducherry']
# districts = ['Pratapgarh (Bihar)','Pratapgarh (Rajasthan)']

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Census App")
        self.setWindowIcon(QIcon('icon.png'))
        self.layout = QGridLayout(self)
        self.region=QComboBox(self)
        self.category=QComboBox(self)
        self.startingYear=QComboBox(self)
        self.endingYear=QComboBox(self)
        self.category.addItem('Male Population')
        self.category.addItem('Female Population')
        self.category.addItem('Total Population')
        for i in states:
            self.region.addItem(f'STATE - {i}')
        for i in districts:
            # TODO if occurences more than one then add brackets
            self.region.addItem(f'DISTRICT - {i[1]}')
        self.region.activated.connect(self.onRegionSelect)
        self.startingYear.activated.connect(self.onStartingYearSelect)
        self.endingYear.activated.connect(self.onYearSelect)
        self.category.activated.connect(self.onYearSelect)

        self.layout.addWidget(QLabel('Select Region',self),0,0,1,1)
        self.layout.addWidget(self.region,0,1,1,3)
        self.layout.addWidget(QLabel('Category',self),1,0,1,1)
        self.layout.addWidget(self.category,1,1,1,3)
        self.layout.addWidget(QLabel('Starting Year',self),2,0,1,1)
        self.layout.addWidget(self.startingYear,2,1,1,1)
        self.layout.addWidget(QLabel('Ending Year',self),2,2,1,1)
        self.layout.addWidget(self.endingYear,2,3,1,1)
        self.setLayout(self.layout)
        self.onRegionSelect()
        self.onYearSelect()
        saveChart=QPushButton('Get Chart')
        saveReport = QPushButton("Generate Report (PDF)")
        saveReport.setStyleSheet('background:rgb(45,125,154);color:#222')
        saveChart.setMinimumHeight(30)
        saveReport.setMinimumHeight(30)
        self.layout.addWidget(saveChart,4,0,1,1)
        self.layout.addWidget(saveReport,4,1,1,3)
        self.layout.addWidget(QSizeGrip(self), 4,3,1,1, Qt.AlignBottom | Qt.AlignRight)

    # Returns state, district from selected region
    def getRegion(self): 
        idx=self.region.currentIndex()
        if idx <= 0: # state selected
            return states[idx],''
        else:
            idx = idx - 1 #26?
            return districts[idx][0],districts[idx][1]

    # Set Starting and Ending Year
    def onRegionSelect(self):
        state,district = self.getRegion()
        years = census.getYearList(state,district)
        startingYear=self.startingYear.currentText()
        endingYear=self.endingYear.currentText()
        self.startingYear.clear()
        self.endingYear.clear()
        for i in years:
            i = str(i)
            self.startingYear.addItem(i)
            self.endingYear.addItem(i)
            # TODO reset previous values
            # print(startingYear,i)
            if startingYear==i:
                self.startingYear.setCurrentText(i)
            if endingYear==i:
                self.endingYear.setCurrentText(i)
        self.onYearSelect()

    # Set Ending Year same as Starting Year
    def onStartingYearSelect(self):
        self.endingYear.setCurrentText(self.startingYear.currentText())
        # TODO set ending years starting from starting year (eg if 2001 then ending year cannot be 1991)
        self.onYearSelect()

    # Draw Chart when Same Year, Graph when different year
    def onYearSelect(self):
        startingYear = int(self.startingYear.currentText())
        # print(startingYear)
        
        endingYear   = int(self.endingYear.currentText())
        if startingYear == endingYear:
            series = QPieSeries()
            state,district = self.getRegion()
            if self.category.currentText()=='Male Population':
                row = census.getMalePopulation(state,district,startingYear)
            elif self.category.currentText()=='Female Population':
                row = census.getFemalePopulation(state,district,startingYear)
            else:
                row = census.getTotalPopulation(state,district,startingYear)
            # print(row)
            demographics = [('Hindu','Orange'),('Muslim','Green'),('Christian','#1E90FF'),('Sikh','Brown'),('Buddhist','#BE7F9D'),('Jain','Salmon'),('Others','Purple'),('Unstated','Grey')]
            for i in range(len(demographics)):
                # print(i,demographics[i][0],row[i+1],)
                slice = series.append(demographics[i][0] + ' (' + str(round((row[i+1]/row[0])*100,2)) + '%)',row[i+1]) # ignoring total
                slice.setBrush(QColor(demographics[i][1]))
                if row[i+1]/row[0] > 0.5: # highlight majority religion
                    slice.setExploded()
                    slice.setPen(QPen(Qt.darkGray, 1))
            chart = QChart()
            chart.addSeries(series)
            chart.legend().setAlignment(Qt.AlignRight)
            chart.setTitle(f'{self.category.currentText()} By Religion, '+(district!='' and f'{district}, ' or '')+f'{state} ({startingYear})')
            font=chart.titleFont()
            font.setBold(True)
            chart.setTitleFont(font)
            # chart.setTitle(chart.title().upper()) # Uppercase?

            chart_view = QChartView(chart)
            chart_view.setRenderHint(QPainter.Antialiasing)
            # chart.setBackgroundBrush(QBrush(QColor("LightGray")))

            self.layout.addWidget(chart_view,3,0,1,4)
        else: # draw graph
            total, year = 0, startingYear
            demographics = [('Total','Crimson'),('Hindu','Orange'),('Muslim','Green'),('Christian','#1E90FF'),('Sikh','Brown'),('Buddhist','#BE7F9D'),('Jain','Salmon'),('Others','Purple'),('Unstated','Grey')]
            rows = [0 for i in demographics] # [[hindu2001,hindu2011,etc],[muslim..],..]
            while year<=endingYear:
                state,district = self.getRegion()
                if self.category.currentText()=='Male Population':
                    row = census.getMalePopulation(state,district,year)
                elif self.category.currentText()=='Female Population':
                    row = census.getFemalePopulation(state,district,year)
                else:
                    row = census.getTotalPopulation(state,district,year)
                for i,_ in enumerate(rows):
                    if rows[i]==0:
                        rows[i]=[]
                    rows[i].append(row[i])
                year+=10
                total = max(total,row[0]//100000)
            sets = [0 for i in rows]
            series = QBarSeries()
            for i,_ in enumerate(sets):
                sets[i]=QBarSet(demographics[i][0])
                sets[i].append(rows[i])
                sets[i].setColor(QColor(demographics[i][1]))
                series.append(sets[i])
            chart = QChart()
            chart.setTitle(f"Decadal {self.category.currentText()} Growth, "+(district!='' and f'{district}, ' or '')+f'{state} ({startingYear}-{endingYear})')
            font=chart.titleFont()
            font.setBold(True)
            chart.setTitleFont(font)
            # chart.setTitle(chart.title().upper()) # Uppercase?

            years = [str(i) for i in range(startingYear,endingYear+1,10)]
            y_axis=QValueAxis()
            y_axis.setRange(0, total)
            y_axis.setTitleText("Population (in lakhs)")
            chart.addSeries(series)
            chart.createDefaultAxes()
            x_axis = QBarCategoryAxis()
            x_axis.setTitleText("Census Year")
            x_axis.append(years)
            x_axis.setRange(str(startingYear), str(endingYear))
            chart.setAxisY(y_axis)
            chart.setAxisX(x_axis)

            chart.legend().setVisible(True)
            chart.legend().setAlignment(Qt.AlignRight)


            chart_view = QChartView(chart)
            chart_view.setRenderHint(QPainter.Antialiasing)
            self.layout.addWidget(chart_view,3,0,1,4)


if __name__=='__main__':
    app = QApplication(sys.argv)
    dark(app)
    win = ModernWindow(MainWindow())
    win.show()
    win.resize(472,552)
    sys.exit(app.exec())