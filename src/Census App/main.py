# Reworked up script

import sys
from api import Census
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtCharts import *
from qtmodern.styles import dark
from qtmodern.windows import ModernWindow

census=Census()
RELIGION = [('Total','Crimson'),('Hindu','Orange'),('Muslim','Green'),('Christian','#1E90FF'),('Sikh','Brown'),('Buddhist','#BE7F9D'),('Jain','Salmon'),('Others','Purple'),('Unstated','Grey')]
GENDER = [('Total','Crimson'),('Male','#0097fa'),('Female','#ff659f')]

# Custom Nested Combo Box
class RegionComboBox(QComboBox):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.parent = parent
        self.__skip_next_hide = False
        self.__activated = True
        self.model = QStandardItemModel()
        treeView = QTreeView(self)
        treeView.setHeaderHidden(True)
        self.setModel(self.model)
        self.model.appendRow(QStandardItem(f'India'))
        self.activated.connect(self.onIndexChanged)
        states = census.getRegionList()

        for state in states:
            parent = QStandardItem(state)
            districts = states[state]
            for district in districts:
                child = QStandardItem(district)
                parent.appendRow(child)
            self.model.appendRow(parent)

        self.setView(treeView)
        self.view().viewport().installEventFilter(self)

    def getRegion(self):
        district = self.view().currentIndex().data()
        state = self.view().currentIndex().parent().data()
        if state == district == None: # value not in model
            state, district = 'India', ''
        if state == None:
            state, district = district, ''
        return state,district

    def onIndexChanged(self):
        if self.__activated:
            self.parent.onRegionSelect()
            self.__activated = False

    def showPopup(self):
        self.setRootModelIndex(QModelIndex())
        super().showPopup()

    def hidePopup(self):
        self.setRootModelIndex(self.view().currentIndex().parent())
        self.setCurrentIndex(self.view().currentIndex().row())
        if self.__skip_next_hide:
            self.__skip_next_hide = False
        else:
            self.__activated = True
            super().hidePopup()

    def selectIndex(self, index):
        self.setRootModelIndex(index.parent())
        self.setCurrentIndex(index.row())

    def eventFilter(self, object, event):
        if event.type() == QEvent.MouseButtonPress and object is self.view().viewport():
            index = self.view().indexAt(event.globalPosition().toPoint())
            self.__skip_next_hide = not self.view().visualRect(index).contains(event.globalPosition().toPoint())
        return False


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Census App")
        self.setWindowIcon(QIcon('icon.png'))
        self.layout = QGridLayout(self)
        self.region = RegionComboBox(self)
        self.distinction=QComboBox(self)
        self.category=QComboBox(self)
        self.startingYear=QComboBox(self)
        self.endingYear=QComboBox(self)
        self.distinction.addItem('Religion')
        self.distinction.addItem('Gender')
        saveChart=QPushButton('Get Chart')
        saveReport = QPushButton("Generate Report (PDF)")
        saveReport.setStyleSheet('background:rgb(45,125,154);color:#222')
        saveChart.setMinimumHeight(30)
        saveReport.setMinimumHeight(30)

        self.layout.addWidget(QLabel('Select Region',self),0,0,1,1)
        self.layout.addWidget(self.region,0,1,1,3)
        self.layout.addWidget(QLabel('Variable',self),1,0,1,1)
        self.layout.addWidget(self.distinction,1,1,1,1)
        self.layout.addWidget(QLabel('Category',self),1,2,1,1)
        self.layout.addWidget(self.category,1,3,1,1)
        self.layout.addWidget(QLabel('Select Region',self),0,0,1,1)
        self.layout.addWidget(self.region,0,1,1,3)
        self.layout.addWidget(QLabel('Starting Year',self),2,0,1,1)
        self.layout.addWidget(self.startingYear,2,1,1,1)
        self.layout.addWidget(QLabel('Ending Year',self),2,2,1,1)
        self.layout.addWidget(self.endingYear,2,3,1,1)
        self.layout.addWidget(saveChart,4,0,1,1)
        self.layout.addWidget(saveReport,4,1,1,3)
        self.layout.addWidget(QSizeGrip(self), 4,3,1,1, Qt.AlignBottom | Qt.AlignRight)
        self.chart_view = None # Chart Widget
        self.setLayout(self.layout)

        self.startingYear.activated.connect(self.onStartingYearSelect)
        self.endingYear.activated.connect(self.onEndingYearSelect)
        self.category.activated.connect(self.onEndingYearSelect)
        self.distinction.activated.connect(self.onVariableSelect)

    def getRegion(self):
        return self.region.getRegion()

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
        self.onVariableSelect()

    def drawPieChart(self,state,district,year):
        category = self.category.currentText()
        var = self.distinction.currentText()
        if var=='Religion':
            VARIABLE = RELIGION
        else:
            VARIABLE = GENDER

        row = census.getPieChart(state,district,year,category)
        
        series = QPieSeries()
        for i in range(1,len(VARIABLE)): # ignoring total
            slice = series.append(VARIABLE[i][0] + ' (' + str(round((row[i]/row[0])*100,2)) + '%)',row[i])
            slice.setBrush(QColor(VARIABLE[i][1]))
            if var=='Religion' and row[i]/row[0] > 0.5: # highlight majority religion
                slice.setExploded()
                slice.setPen(QPen(Qt.darkGray, 1))
        chart = QChart()
        chart.addSeries(series)
        if var=='Religion':
            chart.legend().setAlignment(Qt.AlignRight)
        else:
            chart.legend().setAlignment(Qt.AlignBottom)
        chart.setTitle(f'{category} Population By {var}, '+(district!='' and f'{district}, ' or '')+f'{state} ({year})')
        font=chart.titleFont()
        font.setBold(True)
        chart.setTitleFont(font)
        # chart.setTitle(chart.title().upper()) # Uppercase?

        # if already chart then remove previous chart
        if self.chart_view:
            self.layout.removeWidget(self.chart_view)
            self.chart_view.deleteLater()

        self.chart_view = QChartView(chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        # chart.setBackgroundBrush(QBrush(QColor("LightGray")))

        self.layout.addWidget(self.chart_view,3,0,1,4)

    def drawBarChart(self,state,district,startingYear,endingYear):
        total, year = 0, startingYear
        category = self.category.currentText()
        var = self.distinction.currentText()
        if var=='Religion':
            VARIABLE = RELIGION
        else:
            VARIABLE = GENDER
        rows = [0 for i in VARIABLE] # [[hindu2001,hindu2011,etc],[muslim..],..]
        while year<=endingYear:
            state,district = self.getRegion()
            row=census.getPieChart(state,district,year,category)
            for i,_ in enumerate(rows):
                if rows[i]==0:
                    rows[i]=[]
                rows[i].append(row[i])
            year+=10
            total = max(total,row[0]//1000) # divide by Lakh
        sets = [0 for i in rows]
        series = QBarSeries()
        for i,_ in enumerate(sets):
            sets[i]=QBarSet(VARIABLE[i][0])
            sets[i].append(rows[i])
            sets[i].setColor(QColor(VARIABLE[i][1]))
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
        y_axis.setTitleText("Population (in thousands)")
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

        # if already chart then remove previous chart
        if self.chart_view:
            self.layout.removeWidget(self.chart_view)
            self.chart_view.deleteLater()

        self.chart_view = QChartView(chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.layout.addWidget(self.chart_view,3,0,1,4)

    def onStartingYearSelect(self):
        startingYear = self.startingYear.currentText()
        # if 2001 selected from [1991,2001,2011], ending year is [2001,2011]
        if startingYear != self.endingYear.currentText():
            self.endingYear.clear()
            endingYear = [self.startingYear.itemText(i) for i in range(self.startingYear.count()) if int(self.startingYear.itemText(i))>=int(startingYear)]
            for i in endingYear:
                self.endingYear.addItem(i)
        self.endingYear.setCurrentText(startingYear)
        self.onEndingYearSelect()

    def onVariableSelect(self):
        self.category.clear()
        if self.distinction.currentText()=='Religion':
            items = ['Male','Female','Total']
            for i in items:
                self.category.addItem(i)
        else:
            items = ['Hindu','Muslim','Christian','Sikh','Buddhist','Jain','Others','Unspecified']
            for i in items:
                self.category.addItem(i)
        self.onEndingYearSelect()

    def onEndingYearSelect(self):
        startingYear = int(self.startingYear.currentText())
        endingYear   = int(self.endingYear.currentText())
        state, district = self.getRegion()
        if startingYear == endingYear:
            self.drawPieChart(state,district,startingYear)
        else:
            self.drawBarChart(state,district,startingYear,endingYear)



if __name__=='__main__':
    app = QApplication(sys.argv)
    dark(app)
    win = MainWindow()
    win.region.onIndexChanged()
    win=ModernWindow(win)
    win.show()
    sys.exit(app.exec_())