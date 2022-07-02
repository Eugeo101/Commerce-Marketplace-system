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
        uic.loadUi("mainpage.ui", self)
        # ##print('303')
        # self.error.hide()
        # time.sleep(2)
        self.loaddata() # get and show items
        self.pushButton_5.clicked.connect(self.gotocart) # show cart
        self.lineEdit.textChanged.connect(self.findName) # search
        self.pushButton_2.clicked.connect(self.add) #add item to cart
        self.pushButton.clicked.connect(self.gotoprofile)
        self.pushButton_6.clicked.connect(self.gotohistory)
        self.pushButton_7.clicked.connect(self.gotodeposite)
        self.logoutbutton.clicked.connect(self.gotTologin)

    def gotTologin(self):
        screen = Login()
        widget.addWidget(screen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotohistory(self):
        prof = History()
        widget.addWidget(prof)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoprofile(self):
        prof = viewAccount()
        widget.addWidget(prof)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotodeposite(self):
        prof = Deposit()
        widget.addWidget(prof)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotocart(self):
        ##print('307')
        prof = purchase()
        widget.addWidget(prof)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def findName(self):
        self.error.hide()
        name = self.lineEdit.text().lower()
        for Column in range(self.tableWidget.columnCount()):
            item = self.tableWidget.item(1, Column)
            # if the search is *not* in the item's text *do not hide* the row
            self.tableWidget.setColumnHidden(Column, name not in item.text().lower())

    def add(self):
        # global people
        s = int(self.lineEdit_3.text())
        ##print(s)
        # ##print(people) #items
        name = people[s - 1][ITEM_NAME]
        desc = people[s - 1][DESCRIPTION]
        result = requestServer(ADD_CART, {ITEM_NAME: name, DESCRIPTION: desc})
        ##print(result)
        if (result[RESPONSE] == OK):
            # self.error.show()
            # self.error.setText("Added to cart")
            notify('Added Item', 'labtop: ' + str(name))
        else:
            # self.error.show()
            # self.error.setText("NOT Added to cart")
            notify('Addtion Failed', 'labtop: ' + str(name) + ' already exist in cart')

    def loaddata(self):
        # ##print('336')
        self.error.hide()
        items = requestServer1(GET_ITEMS)
        ##print(items)
        i = 0
        global people #items as list of dictionarys
        l = len(items[ITEMS])
        people = [] #list of items
        person = {}
        # ##print('342')
        # ##print(items)
        while (i < l):
            person[ITEM_NAME] = items[ITEMS][i][0]
            person[DESCRIPTION] = items[ITEMS][i][1]
            person[IMAGE] = items[ITEMS][i][2]
            person[PROCESSOR] = items[ITEMS][i][3]
            person[MEMORY] = items[ITEMS][i][4]
            person[STORAGE] = items[ITEMS][i][5]
            person[MANUFACT] = items[ITEMS][i][6]
            person[PRICE] = items[ITEMS][i][7]
            person[STOCK] = items[ITEMS][i][8]
            people.append(deepcopy(person))
            i += 1
        self.tableWidget.setColumnCount(len(people))
        column = 0
        # ##print(people[0]["name"])
        directory = "assests"
        parent_dir = os.getcwd()
        path = os.path.join(parent_dir, directory, 'Image')
        i = 0
        ##print(len(people))
        for person in people:
            pic = QtGui.QPixmap(path + str(i) + '.jpeg')
            self.label = QtWidgets.QLabel()
            self.label.setPixmap(pic)
            self.tableWidget.setCellWidget(0, column, self.label)
            self.tableWidget.setItem(1, column, QtWidgets.QTableWidgetItem(str(person[ITEM_NAME])))
            self.tableWidget.setItem(2, column, QtWidgets.QTableWidgetItem(str(person[PRICE])))
            self.tableWidget.setItem(3, column, QtWidgets.QTableWidgetItem(str(person[MANUFACT])))
            self.tableWidget.setItem(4, column, QtWidgets.QTableWidgetItem(str(person[DESCRIPTION])))
            self.tableWidget.setItem(5, column, QtWidgets.QTableWidgetItem(str(person[PROCESSOR])))
            self.tableWidget.setItem(6, column, QtWidgets.QTableWidgetItem(str(person[MEMORY])))
            self.tableWidget.setItem(7, column, QtWidgets.QTableWidgetItem(str(person[STORAGE])))
            self.tableWidget.setItem(8, column, QtWidgets.QTableWidgetItem(str(person[STOCK])))
            column = column + 1
            i = i + 1
        self.tableWidget.verticalHeader().setDefaultSectionSize(200)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(200)

class purchase(QDialog):
    def __init__(self):
        super(purchase, self).__init__()
        uic.loadUi("cart.ui",self)
        ##print('385')
        self.load() #load cart of a user
        # self.error.hide()
        ##print('387')
        balance = requestServer1(GET_BALANCE)['balance']
        # total
        total = 0
        for item in cart1:
            total = total + int(item[PRICE]) * int(item[QUANTITY])
        self.label_12.setText(str(total))
        self.label_11.setText(str(balance))
        self.pushButton_5.clicked.connect(self.gotodelete)
        self.pushButton_6.clicked.connect(self.gotoedit)
        self.pushButton_2.clicked.connect(self.back)
        self.pushButton.clicked.connect(self.purch)

    def purch(self):
        # ##print(444)
        total_gold = 0
        for item in cart1:
            total_gold += int(item[PRICE])*int(item[QUANTITY])
        # ##print(total_gold)
        # ##print(type(self.label_11.text()[0:]))
        # ##print(self.label_11.text()[0:])
        # ##print(float(self.label_11.text()[0:]))
        # ##print(int(self.label_11.text()[0:-1]))
        if  total_gold > float(self.label_11.text()):
            # self.error.show()
            # self.error.setText("Not Enough balance")
            notify('Failed Purchase', 'User money is not enough!!')
        else:
            # ##print(452)
            cart2 = requestServer1(GET_ITEMS)
            items_from_dp = []
            i=0
            l = len(cart2[ITEMS])
            person={}
            while (i < l):
                person[ITEM_NAME] = cart2[ITEMS][i][0]
                person[DESCRIPTION] = cart2[ITEMS][i][1]
                person[IMAGE] = cart2[ITEMS][i][2]
                person[PROCESSOR] = cart2[ITEMS][i][3]
                person[MEMORY] = cart2[ITEMS][i][4]
                person[STORAGE] = cart2[ITEMS][i][5]
                person[MANUFACT] = cart2[ITEMS][i][6]
                person[PRICE] = cart2[ITEMS][i][7]
                person[STOCK] = cart2[ITEMS][i][8]
                items_from_dp.append(deepcopy(person))
                i += 1
            # ##print(cart1)
            # ##print(469)
            # ##print(items_from_dp)

            #get updated stock into cart1
            for item in items_from_dp: #user [1, 20]
                for user_cart in cart1: #user [1, 2, 3]
                    if (item[ITEM_NAME] == user_cart[ITEM_NAME]) and (item[DESCRIPTION] == user_cart[DESCRIPTION]):
                        user_cart[STOCK] = item[STOCK]
            self.tableWidget_2.setColumnCount(len(cart1))
            column = 0
            ##print('475')
            #table
            for person in cart1:
                self.tableWidget_2.setItem(8,column, QtWidgets.QTableWidgetItem(str(person[STOCK])))
                column =column+1
            self.tableWidget_2.verticalHeader().setDefaultSectionSize(200)
            self.tableWidget_2.horizontalHeader().setDefaultSectionSize(200)
            pur_acc = True
            ##print('481')
            for s in cart1:
                if s[STOCK] < s[QUANTITY]:
                    pur_acc = False
                    # self.error.show()
                    # self.error.setText("Not Enough Items In Stock")
                    notify("Failed Purchase", 'Not Enough Items In Stock')
            if (pur_acc):
                requestServer(PURCHASE,{ITEMS :cart1})
                self.back()

    def back(self):
        ##print('487')
        prof = cart()
        widget.addWidget(prof)
        widget.setCurrentIndex(widget.currentIndex()+1)


    def load(self):
        # self.error.hide()
        ##print('450')
        cart2 = requestServer1(GET_CART)
        i = 0
        l = len(cart2["items"])
        # ##print(l)
        global cart1
        cart1 = []
        dic = {}
        if (l == 0):
            # ##print('461')
            self.errorlabel.setText("THE CART IS EMPTY!")
            # ##print('463')
            pass
        else:
            ##print('474')
            while (i < l):
                dic[ITEM_NAME] = cart2["items"][i][0]
                dic[DESCRIPTION] = cart2["items"][i][1]
                dic[IMAGE] = cart2["items"][i][2]
                dic[PROCESSOR] = cart2["items"][i][3]
                dic[MEMORY] = cart2["items"][i][4]
                dic[STORAGE] = cart2["items"][i][5]
                dic[MANUFACT] = cart2["items"][i][6]
                dic[PRICE] = cart2["items"][i][7]
                dic[STOCK] = cart2["items"][i][8]
                dic[QUANTITY] = 1
                cart1.append(deepcopy(dic))
                i += 1
            # ##print(cart1)
            self.tableWidget_2.setColumnCount(len(cart1))
            column = 0
            directory = "assests"
            parent_dir = os.getcwd()
            path = os.path.join(parent_dir, directory, 'Cart')
            i = 0
            ##print(529)
            ##print(cart1)
            for person in cart1:  # data
                pic = QtGui.QPixmap(path + str(i) + '.jpeg')
                self.label = QtWidgets.QLabel()
                self.label.setPixmap(pic)
                self.tableWidget_2.setCellWidget(0, column, self.label)
                self.tableWidget_2.setItem(1, column, QtWidgets.QTableWidgetItem(str(person[ITEM_NAME])))
                self.tableWidget_2.setItem(2, column, QtWidgets.QTableWidgetItem(str(person[PRICE])))
                self.tableWidget_2.setItem(3, column, QtWidgets.QTableWidgetItem(str(person[MANUFACT])))
                self.tableWidget_2.setItem(4, column, QtWidgets.QTableWidgetItem(str(person[DESCRIPTION])))
                self.tableWidget_2.setItem(5, column, QtWidgets.QTableWidgetItem(str(person[PROCESSOR])))
                self.tableWidget_2.setItem(6, column, QtWidgets.QTableWidgetItem(str(person[MEMORY])))
                self.tableWidget_2.setItem(7, column, QtWidgets.QTableWidgetItem(str(person[STORAGE])))
                self.tableWidget_2.setItem(8, column, QtWidgets.QTableWidgetItem(str(person[STOCK])))
                self.tableWidget_2.setItem(9, column, QtWidgets.QTableWidgetItem(str(person[QUANTITY])))
                column = column + 1
                i = i + 1
            self.tableWidget_2.verticalHeader().setDefaultSectionSize(200)
            self.tableWidget_2.horizontalHeader().setDefaultSectionSize(200)


    def gotoedit(self):
        ##print('557')
        productId = int(self.delete_2.text()) - 1
        try:
            ##print('568')
            quantity = int(self.edit_2.text())
            if quantity <= 0:
                quantity = 1
            ##print(cart1)
            cart1[productId][QUANTITY] = quantity  # in case we changed quantity
            ##print(cart1)
        except:
            quantity = 1
        ##print('554')
        total_gold = 0
        for item in cart1:
            total_gold = total_gold + int(item[PRICE]) * int(item[QUANTITY])
        ##print(574)
        ##print(total_gold)
        self.label_12.setText(str(total_gold))
        self.tableWidget_2.setColumnCount(len(cart1))
        column = 0
        ##print('564')
        for person in cart1:
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
        productId = int(self.delete_2.text()) - 1
        name = cart1[productId][ITEM_NAME]
        DESC = cart1[productId][DESCRIPTION]
        requestServer(REMOVE_CART,{ITEM_NAME:name,DESCRIPTION:DESC})
        del cart1[productId]
        total_gold = 0
        for item in cart1:
            total_gold += int(item[PRICE])*int(item[QUANTITY])
            # cart1[productId][PRICE] = int(item[PRICE]) * int(item[QUANTITY])
        ##print(613)
        ##print(total_gold)
        self.label_12.setText(str(total_gold))
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
            column = column + 1
        self.tableWidget_2.verticalHeader().setDefaultSectionSize(200)
        self.tableWidget_2.horizontalHeader().setDefaultSectionSize(200)


# main
app = QApplication(sys.argv)
cart1=[] #cart
people=[] #items
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
