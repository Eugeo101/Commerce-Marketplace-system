import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets
from client import *
from copy import deepcopy



class cart(QDialog):
    def __init__(self):
        super(cart, self).__init__()
        loadUi("main_2.ui",self)
        self.loaddata()
        self.pushButton_5.clicked.connect(self.gotocart)
        self.lineEdit.textChanged.connect(self.findName)
        self.pushButton_2.clicked.connect(self.add)


    def gotocart(self):
        prof = purchase()
        widget.addWidget(prof)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def findName(self):
        name = self.lineEdit.text().lower()
        for Column in range(self.tableWidget.columnCount()):
            item = self.tableWidget.item(1, Column)
            # if the search is *not* in the item's text *do not hide* the row
            self.tableWidget.setColumnHidden(Column, name not in item.text().lower())
    def add (self):
        global people
        people=[]
        s = int(self.lineEdit_3.text())-1
        y = int(self.lineEdit_2.text())
        name=people[S][ITEM_NAME]
        desc =people[S][DESCRIPTION]
        Socket.requestServer(ADD_CART,{ITEM_NAME:name,DESCRIPTION:desc})




    def loaddata(self):
        items =Socket.requestServer(GET_ITEMS)
        i=0
        x= len(items[ITEMS])
        people=[]
        person={}
        while(i<x):
            person[ITEM_NAME]=items["item"][i][0]
            person[DESCRIPTION] = items["item"][i][1]
            person[IMAGE] = items["item"][i][2]
            person[PROCESSOR] = items["item"][i][3]
            person[MEMORY] = items["item"][i][4]
            person[STORAGE] = items["item"][i][5]
            person[MANUFACT] = items["item"][i][6]
            person[PRICE] = items["item"][i][7]
            person[STOCK] = items["item"][i][8]
            people.append(deepcopy(person))
            i+=1
        self.tableWidget.setColumnCount(len(people))
        column =0
        print(people[0]["name"])
        for person in people :
            pic = QtGui.QPixmap(person[IMAGE])
            self.label = QtWidgets.QLabel()
            self.label.setPixmap(pic)
            self.tableWidget.setCellWidget(0,column, self.label)
            self.tableWidget.setItem(1,column, QtWidgets.QTableWidgetItem(str(person[ITEM_NAME])))
            self.tableWidget.setItem(2,column, QtWidgets.QTableWidgetItem(str(person[PRICE])))
            self.tableWidget.setItem(3,column, QtWidgets.QTableWidgetItem(str(person[MANUFACT])))
            self.tableWidget.setItem(4,column, QtWidgets.QTableWidgetItem(str(person[DESCRIPTION])))
            self.tableWidget.setItem(5,column, QtWidgets.QTableWidgetItem(str(person[PROCESSOR])))
            self.tableWidget.setItem(6,column, QtWidgets.QTableWidgetItem(str(person[MEMORY])))
            self.tableWidget.setItem(7,column, QtWidgets.QTableWidgetItem(str(person[STORAGE])))
            self.tableWidget.setItem(8,column, QtWidgets.QTableWidgetItem(str(person[STOCK])))
            column =column+1
        self.tableWidget.verticalHeader().setDefaultSectionSize(200)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(200)

class purchase(QDialog):
    def __init__(self):
        super(purchase, self).__init__()
        loadUi("main_3.ui",self)
        self.load()
        self.error.hide()
        balance=Socket.requestServer(GET_BALANCE)
        self.label_11.setText(str(balance))
        self.pushButton_5.clicked.connect(self.gotodelete)
        self.pushButton_6.clicked.connect(self.gotoedit)
        self.pushButton_2.clicked.connect(self.back)
        self.pushButton.clicked.connect(self.purch)

    def purch(self):
        total_gold = 0
        for item in cart1:
            total_gold += int(item[PRICE])*int(item[QUANTITY])
        if  total_gold > int(self.label_11.text()):
            self.error.show()
            self.error.setText("Not Enough balance")
        else :
            cart2 = Socket.requestServer(GET_CART)
            i=0
            x= len(cart2[ITEMS])
            person={}
            while(i<x):
                person[ITEM_NAME]=items["item"][i][0]
                person[DESCRIPTION] = items["item"][i][1]
                person[IMAGE] = items["item"][i][2]
                person[PROCESSOR] = items["item"][i][3]
                person[MEMORY] = items["item"][i][4]
                person[STORAGE] = items["item"][i][5]
                person[MANUFACT] = items["item"][i][6]
                person[PRICE] = items["item"][i][7]
                person[STOCK] = items["item"][i][8]
                cart2.append(deepcopy(person))
                i+=1
            for c in cart2:
                for x in cart1 :
                    if c[ITEM_NAME]==x[ITEM_NAME] && c[DESCRIPTION]==x[DESCRIPTION]:
                        x[STOCK] =c[STOCK]
            self.tableWidget_2.setColumnCount(len(cart1))
            column =0
            for person in cart1 :
                self.tableWidget_2.setItem(8,column, QtWidgets.QTableWidgetItem(str(person[STOCK])))
                column =column+1
            self.tableWidget_2.verticalHeader().setDefaultSectionSize(200)
            self.tableWidget_2.horizontalHeader().setDefaultSectionSize(200)

            pur_acc = True

            for s in cart1 :
                if s[STOCK] < s[QUANTITY]:
                    pur_acc =False
                    self.error.show()
                    self.error.setText("Not Enough Items In Stock")

            if (pur_acc):
                Socket.requestServer(PURCHASE,{ITEMS :cart1})

    def back(self):
        prof = cart()
        widget.addWidget(prof)
        widget.setCurrentIndex(widget.currentIndex()+1)


    def load(self):
        global cart1
        cart1=[]
        cart1 = Socket.requestServer(GET_CART)
        i=0
        x= len(cart1[ITEMS])
        person={}
        while(i<x):
            person[ITEM_NAME]=items["item"][i][0]
            person[DESCRIPTION] = items["item"][i][1]
            person[IMAGE] = items["item"][i][2]
            person[PROCESSOR] = items["item"][i][3]
            person[MEMORY] = items["item"][i][4]
            person[STORAGE] = items["item"][i][5]
            person[MANUFACT] = items["item"][i][6]
            person[PRICE] = items["item"][i][7]
            person[STOCK] = items["item"][i][8]
            person[QUANTITY] = 1


            cart1.append(deepcopy(person))
            i+=1

        self.tableWidget_2.setColumnCount(len(cart1))
        column =0
        for person in cart1 :
            pic = QtGui.QPixmap(person[IMAGE])
            self.label = QtWidgets.QLabel()
            self.label.setPixmap(pic)
            self.tableWidget_2.setCellWidget(0,column, self.label)
            self.tableWidget_2.setItem(1,column, QtWidgets.QTableWidgetItem(str(person[ITEM_NAME])))
            self.tableWidget_2.setItem(2,column, QtWidgets.QTableWidgetItem(str(person[PRICE])))
            self.tableWidget_2.setItem(3,column, QtWidgets.QTableWidgetItem(str(person[MANUFACT])))
            self.tableWidget_2.setItem(4,column, QtWidgets.QTableWidgetItem(str(person[DESCRIPTION])))
            self.tableWidget_2.setItem(5,column, QtWidgets.QTableWidgetItem(str(person[PROCESSOR])))
            self.tableWidget_2.setItem(6,column, QtWidgets.QTableWidgetItem(str(person[MEMORY])))
            self.tableWidget_2.setItem(7,column, QtWidgets.QTableWidgetItem(str(person[STORAGE])))
            self.tableWidget_2.setItem(8,column, QtWidgets.QTableWidgetItem(str(person[STOCK])))
            self.tableWidget_2.setItem(9,column, QtWidgets.QTableWidgetItem(str(person[QUANTITY])))
            column =column+1
        self.tableWidget_2.verticalHeader().setDefaultSectionSize(200)
        self.tableWidget_2.horizontalHeader().setDefaultSectionSize(200)


    def gotoedit(self):
        c = int(self.delete_2.text())
        x = int(self.edit_2.text())

        if x<=0:
            x=1
        cart1[c][QUANTITY]= x
        total_gold = 0
        for item in cart1:
            total_gold += int(item[PRICE])*int(item[QUANTITY])
        self.label_12.setText(str(total_gold)+" "+"$")
        self.tableWidget_2.setColumnCount(len(cart1))
        column =0
        for person in cart1 :
            pic = QtGui.QPixmap(person[IMAGE])
            self.label = QtWidgets.QLabel()
            self.label.setPixmap(pic)
            self.tableWidget_2.setCellWidget(0,column, self.label)
            self.tableWidget_2.setItem(1,column, QtWidgets.QTableWidgetItem(str(person[ITEM_NAME])))
            self.tableWidget_2.setItem(2,column, QtWidgets.QTableWidgetItem(str(person[PRICE])))
            self.tableWidget_2.setItem(3,column, QtWidgets.QTableWidgetItem(str(person[MANUFACT])))
            self.tableWidget_2.setItem(4,column, QtWidgets.QTableWidgetItem(str(person[DESCRIPTION])))
            self.tableWidget_2.setItem(5,column, QtWidgets.QTableWidgetItem(str(person[PROCESSOR])))
            self.tableWidget_2.setItem(6,column, QtWidgets.QTableWidgetItem(str(person[MEMORY])))
            self.tableWidget_2.setItem(7,column, QtWidgets.QTableWidgetItem(str(person[STORAGE])))
            self.tableWidget_2.setItem(8,column, QtWidgets.QTableWidgetItem(str(person[STOCK])))
            self.tableWidget_2.setItem(9,column, QtWidgets.QTableWidgetItem(str(person[QUANTITY])))
            column =column+1
        self.tableWidget_2.verticalHeader().setDefaultSectionSize(200)
        self.tableWidget_2.horizontalHeader().setDefaultSectionSize(200)



    def gotodelete(self):
        c = int(self.delete_2.text())-1
        name=cart1[c][ITEM_NAME]
        DESC=cart1[c][DESCRIPTION]
        Socket.requestServer(REMOVE_CART,{ITEM_NAME:name,DESCRIPTION;DESC})
        del cart1[c]
        total_gold = 0
        for item in cart1:
            total_gold += int(item[PRICE])*int(item[QUANTITY])
        self.label_12.setText(str(total_gold)+" "+"$")
        self.tableWidget_2.setColumnCount(len(cart1))
        column =0
        for person in cart1 :
            pic = QtGui.QPixmap(person[IMAGE])
            self.label = QtWidgets.QLabel()
            self.label.setPixmap(pic)
            self.tableWidget_2.setCellWidget(0,column, self.label)
            self.tableWidget_2.setItem(1,column, QtWidgets.QTableWidgetItem(str(person[ITEM_NAME])))
            self.tableWidget_2.setItem(2,column, QtWidgets.QTableWidgetItem(str(person[PRICE])))
            self.tableWidget_2.setItem(3,column, QtWidgets.QTableWidgetItem(str(person[MANUFACT])))
            self.tableWidget_2.setItem(4,column, QtWidgets.QTableWidgetItem(str(person[DESCRIPTION])))
            self.tableWidget_2.setItem(5,column, QtWidgets.QTableWidgetItem(str(person[PROCESSOR])))
            self.tableWidget_2.setItem(6,column, QtWidgets.QTableWidgetItem(str(person[MEMORY])))
            self.tableWidget_2.setItem(7,column, QtWidgets.QTableWidgetItem(str(person[STORAGE])))
            self.tableWidget_2.setItem(8,column, QtWidgets.QTableWidgetItem(str(person[STOCK])))
            self.tableWidget_2.setItem(9,column, QtWidgets.QTableWidgetItem(str(person[QUANTITY])))
            column =column+1
        self.tableWidget_2.verticalHeader().setDefaultSectionSize(200)
        self.tableWidget_2.horizontalHeader().setDefaultSectionSize(200)

# main
app = QApplication(sys.argv)
cart1=[]
people=[]
dict =[]
welcome = cart()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(900)
widget.setFixedWidth(1200)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
