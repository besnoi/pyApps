import sys

from api import Census
from PySide6.QtCore import QSize, Qt, QUrl
from PySide6.QtWidgets import *
from PySide6.QtWebEngineWidgets import *
from PySide6.QtGui import QColor,QPainter,QPen,QFont,QIcon
from qtmodern.styles import dark
from qtmodern.windows import ModernWindow

census = Census()
GENDER = {'males':'#0097fa','females':'#ff659f'}
RELIGION = {'Hindu':'#ff4500','Muslim':'#009000','Christian':'#1E90FF','Sikh':'#964B00','Buddhist':'#BE7F9D','Jain':'#fa8072','Other':'#A020F0','Unstated':'#808080'}

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Census App")
        self.setWindowIcon(QIcon('icon.png'))
        self.layout = QGridLayout(self)
        self.states=QComboBox(self)
        self.year=QComboBox(self)
        self.category=QComboBox(self)
        self.indicator=QComboBox(self)
        self.browser = QWebEngineView()
        # self.states.addItem('India')
        self.category.addItems(['Population By Religion','Population By Gender'])
        states = census.getRegionList()
        self.states.addItem("India") # We need India to be on first always
        for i in states:
            self.states.addItem(i)
        self.layout.addWidget(QLabel('Select State',self),0,0,1,1)
        self.layout.addWidget(self.states,0,1,1,1)
        self.layout.addWidget(QLabel('Select Year',self),0,2,1,1)
        self.layout.addWidget(self.year,0,3,1,1)
        self.layout.addWidget(QLabel('Select Category',self),1,0,1,1)
        self.layout.addWidget(self.category,1,1,1,3)
        self.layout.addWidget(QLabel('Select Indicator',self),2,0,1,1)
        self.layout.addWidget(self.indicator,2,1,1,3)
        self.layout.addWidget(self.browser,3,0,1,4)
        self.layout.addWidget(QSizeGrip(self), 3,3,1,1, Qt.AlignBottom | Qt.AlignRight)
        self.setLayout(self.layout)

        self.states.activated.connect(self.onStateSelect)
        self.year.activated.connect(self.onYearSelect) # TODO
        self.category.activated.connect(self.onCategorySelect)
        self.indicator.activated.connect(self.onIndicatorSelect)
        self.onStateSelect()

    def onStateSelect(self):
        years = census.getYearList(self.states.currentText(),'')
        prev = self.year.currentText() or str(years[-1])
        self.year.clear()
        for i in years:
            print(i)
            self.year.addItem(str(i))
        self.year.setCurrentText(prev) # restore previous value
        self.onCategorySelect()

    def onYearSelect(self):
        year = int(self.year.currentText())
        prev = self.states.currentText()
        states = census.getRegionList(year)
        self.states.clear()
        self.states.addItem("India") # We need India to be on first always
        for i in states:
            print(i)
            self.states.addItem(i)
        self.states.setCurrentText(prev)
        self.onCategorySelect()


    def onCategorySelect(self):
        self.indicator.clear()
        if self.category.currentText()=='Population By Religion':
            sex = ['People','Women','Men']
            for i in sex:
                for j in RELIGION:
                    if j=='Unstated':
                        j = 'Unstated or No'
                    self.indicator.addItem(f'{i} professing {j} Religion'+(j=='Other' and 's' or '')+' (%)')
        elif self.category.currentText()=="Population By Gender":
            self.indicator.addItems(['Male Population (%)','Female Population (%)'])
        self.onIndicatorSelect()

    def onIndicatorSelect(self):
        state = self.states.currentText()
        year,category,indicator = self.year.currentText(),self.category.currentText(),self.indicator.currentText()
        
        isNegative = True

        if 'Female' in indicator or 'Women' in indicator:
            sex = 'females'
        elif 'Male' in indicator or 'Men' in indicator:
            sex = 'males'
        else:
            sex = 'total'

        if category == 'Population By Religion':
            for i in RELIGION:
                if i in indicator:
                    if i=='Unstated':
                        religion = 'atheist'
                    else:
                        religion = i.lower()
                    maxColor = RELIGION[i]
                    break
        else:
            maxColor = GENDER[sex]
            religion = 'total'

        data = census.getChoropleth(year,state,religion,sex)
        if state=='India':
            if int(year)<2000: # for 2021 census we will use latest 2019 map
                mapURL = 'https://besnoi.github.io/maps/json/india-1999.json'
            else:
                mapURL = 'https://besnoi.github.io/maps/json/india-2013.json'
        elif state=='Andhra Pradesh' and int(year)<2014: # andhra pradesh was bifurcated on 2014
            mapURL = 'https://besnoi.github.io/maps/json/andhra-pradesh-2014.json'
        else:
            mapURL = 'https://besnoi.github.io/maps/json/'+state.lower()+'.json'

        if int(year)<2000 and state in ['Bihar','Madhya Pradesh','Uttar Pradesh']:
            mapURL = f'https://besnoi.github.io/maps/json/{state.lower()}-1999.json'
        elif int(year)<2011 and state in ['Bihar','Madhya Pradesh']:
            mapURL = f'https://besnoi.github.io/maps/json/{state.lower()}-2001.json'

        print(data)
            

        number = 'Percentage' # i assume all data will be in percentage but subject to change?

        html = ("<style>body{overflow-y:hidden}#container{height: 500px; min-width: 310px; max-width: 800px; margin: 0 auto;}.loading{margin-top: 10em; text-align: center; color: gray;}</style><script src='https://code.highcharts.com/maps/highmaps.js'></script><div id='container'></div><script>(async ()=>{const topology=await fetch( '"+mapURL+"' ).then(response=> response.json()); const data="+
        str(data)+
        "; Highcharts.mapChart('container',{chart:{map: topology}, title:{text: '"+indicator[:-4]+" in "+state+" (%)'}, subtitle:{text: '"+state+(' (excluding Jammu and Kashmir)' if year=='1991' and state=='India' else '')+ ": "+str(data[0][1])+"',align: 'center',verticalAlign: 'bottom'}, legend:{layout: 'vertical', align: 'right', verticalAlign: 'middle'},mapNavigation:{enabled: true, buttonOptions:{verticalAlign: 'bottom'}}, colorAxis:{align: 'right',verticalMiddle:'middle',min: 0, minColor: '#ffffff', maxColor: '"+maxColor+"'}, credits:{enabled:false}, series: [{data: data, name: '"+number+"', states:{hover:{color: '#BADA55'}}, dataLabels:{enabled: true, format: '{point.name}'}}]});})();</script>")
        # print(html)
        self.browser.setHtml(html)
        print(data[0][1])


if __name__=='__main__':
    app = QApplication(sys.argv)
    # dark(app)
    # app.setStyleSheet(qtvsc.load_stylesheet(qtvsc.Theme.LIGHT_VS))
    win = MainWindow()
    win.show()
    win.resize(640,646)
    sys.exit(app.exec())
