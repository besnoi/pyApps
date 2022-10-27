import sys

from api import NHFSReport
from PySide6.QtCore import QSize, Qt, QUrl
from PySide6.QtWidgets import *
from PySide6.QtWebEngineWidgets import *
from PySide6.QtGui import QColor,QPainter,QPen,QFont,QIcon
from qtmodern.styles import dark
from qtmodern.windows import ModernWindow
import qtvscodestyle as qtvsc

report = NHFSReport()
CATEGORIES = report.getIndicators()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NHFS App")
        self.setWindowIcon(QIcon('icon.png'))
        self.layout = QGridLayout(self)
        self.year=QComboBox(self)
        self.typology=QComboBox(self)
        self.category=QComboBox(self)
        self.indicator=QComboBox(self)
        self.browser = QWebEngineView()
        self.year.addItem('NFHS-5 (2019-21)')
        self.typology.addItems(['Urban','Rural','Total'])
        for i in CATEGORIES:
            self.category.addItem(i)
        self.indicator.addItem('Women age 15 years and above who consume alcohol (%)')
        self.layout.addWidget(QLabel('Survey Year',self),0,0,1,1)
        self.layout.addWidget(self.year,0,1,1,1)
        self.layout.addWidget(QLabel('Select Typology',self),0,2,1,1)
        self.layout.addWidget(self.typology,0,3,1,1)
        self.layout.addWidget(QLabel('Select Category',self),1,0,1,1)
        self.layout.addWidget(self.category,1,1,1,3)
        self.layout.addWidget(QLabel('Select Indicator',self),2,0,1,1)
        self.layout.addWidget(self.indicator,2,1,1,3)
        self.layout.addWidget(self.browser,3,0,1,4)
        self.layout.addWidget(QSizeGrip(self), 3,3,1,1, Qt.AlignBottom | Qt.AlignRight)
        self.setLayout(self.layout)

        self.category.activated.connect(self.onCategorySelect)
        self.typology.activated.connect(self.onIndicatorSelect)
        self.indicator.activated.connect(self.onIndicatorSelect)
        self.onCategorySelect()

    def onCategorySelect(self):
        indicators = CATEGORIES[self.category.currentText()]
        self.indicator.clear()
        for i in indicators:
            self.indicator.addItem(i)
        self.onIndicatorSelect()

    def onIndicatorSelect(self):
        year,category,indicator,typology = self.year.currentText(),self.category.currentText(),self.indicator.currentText(),self.typology.currentText()
        isNegative = False # is a negative thing? like gender violence?
        negativeWords = ['hypertension','violence','tobacco','mortality','fertility','sterilization','anaemia','sugar','nutritional','diseases','unmet','wasted','stunted','overweight','underweight']
        for word in negativeWords:
            if word in category.lower() or word in indicator.lower():
                isNegative = True
                break

        if '%' in indicator:
            number = 'Percentage'
        else:
            number = 'Rate'

        data = report.getData(category,indicator,typology)

        html = ("<style>body{overflow-y:hidden}#container{height: 500px; min-width: 310px; max-width: 800px; margin: 0 auto;}.loading{margin-top: 10em; text-align: center; color: gray;}</style><script src='https://code.highcharts.com/maps/highmaps.js'></script><div id='container'></div><script>(async ()=>{const topology=await fetch( 'https://code.highcharts.com/mapdata/countries/in/custom/in-all-disputed.topo.json' ).then(response=> response.json()); const data="+
        str(data)+
        "; Highcharts.mapChart('container',{chart:{map: topology}, title:{text: '"+indicator+"'}, subtitle:{text: 'India: "+str(data[0][1])+"',align: 'center',verticalAlign: 'bottom'}, legend:{layout: 'vertical', align: 'right', verticalAlign: 'middle'},mapNavigation:{enabled: true, buttonOptions:{verticalAlign: 'bottom'}}, colorAxis:{align: 'right',verticalMiddle:'middle',min: 0 "+(isNegative and ", minColor: '#efecf3', maxColor: '#ff0000'" or "")+"}, series: [{data: data, name: '"+number+"', states:{hover:{color: '#BADA55'}}, dataLabels:{enabled: false, format: '{point.name}'}}]});})();</script>")
        print(html)
        self.browser.setHtml(html)


if __name__=='__main__':
    app = QApplication(sys.argv)
    # dark(app)
    app.setStyleSheet(qtvsc.load_stylesheet(qtvsc.Theme.LIGHT_VS))
    win = ModernWindow(MainWindow())
    win.show()
    win.resize(640,646)
    sys.exit(app.exec())