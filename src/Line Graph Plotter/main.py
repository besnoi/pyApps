'''
    Line Graph Plotter with PyQt5 / Neir
    
    Part of 100 GUI Apps Challenge
    (https://github.com/besnoi/pyApps)

    Challenge Rules :
        1. App must be useful
        2. App must be beautiful
        3. App must be short (<500 LOC)
    
    And lastly no Plagiarism :D
'''

import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import QIcon
import qdarktheme
from pyqtgraph import PlotWidget as QPlotWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Line Graph Plotter')
        self.setWindowIcon(QIcon('linegraph.ico'))

        label1 = QLabel('Enter Horizontal Values:', self)
        label2 = QLabel('Enter Vertical Values:', self)
        self.horValues = QLineEdit(self)
        self.verValues = QLineEdit(self)
        self.horValues.setPlaceholderText('eg. 1,2,3,4')
        self.verValues.setPlaceholderText('eg. 10,50,20,70')
        plotBtn=QPushButton('Plot',self)
        clearBtn=QPushButton('Clear',self)
        # plotBtn.setMinimumSize(100,55)
        plotBtn.setStyleSheet('color:rgb(55,54,59);background-color: rgb(68,138,200);')

        self.graphWidget = QPlotWidget(self)
        self.graphWidget.setBackground('#323232')

        layout = QGridLayout()
        layout.addWidget(label1, 0, 0)
        layout.addWidget(self.horValues, 0, 1, 1, 3)
        layout.addWidget(plotBtn, 0, 4, 1, 1)
        layout.addWidget(label2, 1, 0)
        layout.addWidget(self.verValues, 1, 1, 1, 3)
        layout.addWidget(clearBtn, 1, 4, 1, 1)
        layout.addWidget(self.graphWidget, 2, 0, 1, 5)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        # plot default values
        self.graphWidget.plot([1, 2, 3, 4], [10,50,20,70],symbol ='o', symbolPen ='w', symbolBrush = 0.2)

        plotBtn.clicked.connect(self.plot)
        clearBtn.clicked.connect(self.graphWidget.clear)

    # helper function to check if string contains only ., and numbers
    def isList(self,s):
        for i in s:
            if not i.isnumeric() and i!=',' and i!='.':
                return False
        return True
    def plot(self):
        try:
            horValues = eval(f'[{self.horValues.text()}]')
            verValues = eval(f'[{self.verValues.text()}]')
            self.graphWidget.plot(horValues, verValues,symbol ='o', symbolPen ='w', symbolBrush = 0.2)
        except SyntaxError:
            return QMessageBox.critical(self,'Error','Invalid Input!\nOnly Numbers Allowed')
        except:
            return QMessageBox.critical(self,'Error',"Couldn't plot the graph\nCheck input again!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet())
    main = MainWindow()
    main.setMinimumSize(400,400)
    main.show()
    app.exec()
