import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from client import *

class History(QDialog):
    def __init__(self):
        super("History",self).__init__()
        uic.loadUi("History.ui",self)

    def loaddata(self):
        History = Socket.requestServer(HISTORY)

        self.tableWidget.setColumnCount(len(History[HISTORY]))
        row =0
        for record in History[HISTORY]:

            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(row+1)))
            self.tableWidget.setItem(row,1, QtWidgets.QTableWidgetItem(str(record[0])))
            self.tableWidget.setItem(row,2, QtWidgets.QTableWidgetItem(str(record[1])))
            self.tableWidget.setItem(row,3, QtWidgets.QTableWidgetItem(str(record[2])))
            self.tableWidget.setItem(row,4, QtWidgets.QTableWidgetItem(str(record[3])))
            self.tableWidget.setItem(row,5, QtWidgets.QTableWidgetItem(str(record[4])))

            row =row+1
        self.tableWidget.verticalHeader().setDefaultSectionSize(200)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(200)


#main
app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
widget.setFixedHeight(900)
widget.setFixedWidth(1200)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")