import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from client import *

class History(QDialog):
    def _init_(self):
        super(History,self)._init_()
        uic.loadUi("History.ui",self)
        #self.backbutton.clicked.connect(self.gotomainpage)
        self.loaddata()

    def loaddata(self):

        #History = Socket.requestServer(HISTORY)
        #self.tableWidget.setColumnCount(len(History[HISTORY]))

        row = 0
        HISTORY = "HISTORY" ##delete
        History = {HISTORY:[("lap1","this is lap1","3","2022-2-21","300$"),("lap2","this is lap2","4","2022-2-21","400$")]} ##delete
        self.tableWidget.setRowCount(len(History[HISTORY]))
        for record in History[HISTORY]:

            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(record[0])))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(record[1])))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(record[2])))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(record[3])))
            self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(record[4])))

            row = row+1

        #self.tableWidget.verticalHeader().setDefaultSectionSize(200)
        #self.tableWidget.horizontalHeader().setDefaultSectionSize(200)

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