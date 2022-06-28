import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets




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
        for row in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row, 0)
            # if the search is *not* in the item's text *do not hide* the row
            self.tableWidget.setRowHidden(row, name not in item.text().lower())
    def add (self):
        s = self.lineEdit_3.text()
        y = int(self.lineEdit_2.text())
        global dict
        people = [{"name": "Dell", "price": 45, "amount": "50"}, {"name": "hp", "price": 10, "amount": "100"},
                  {"name": "oppo", "price": 100, "amount": "50"}
            , {"name": "screen", "price": 10, "amount": "50"}, {"name": "buttery", "price": 5, "amount": "50"},
                  {"name": "DC_charge", "price": 57, "amount": "50"}
                  ]

        if len(dict)==0:
            index_1= next((index for (index, d) in enumerate(people) if d["name"] == s), None)
            if int(people[index_1]["amount"])<y :
                print("ahmed")
            else:
                dict.append(next(x for x in people if x["name"] == s))
                dict[0]["quantity"] = y
                dict[0]["total"] = y * dict[0]["price"]
                print(dict)
                # self.tableWidget_2.setRowCount(len(dict))
                # row =0
                # for person in dict :
                #     self.tableWidget_2.setItem(row,0, QtWidgets.QTableWidgetItem(person["name"]))
                #     self.tableWidget_2.setItem(row,1, QtWidgets.QTableWidgetItem(str(person["price"])))
                #     self.tableWidget_2.setItem(row,2, QtWidgets.QTableWidgetItem(str(person["quantity"])))
                #     self.tableWidget_2.setItem(row,3, QtWidgets.QTableWidgetItem(str(person["total"])))
                #     row =row+1

        else:
            list_of_all_values = [value for elem in dict
                                  for value in elem.values()]
            value =s
            if value in list_of_all_values:
                if next(x for x in dict if x["name"] == s) in dict:
                    tom_index = next((index for (index, d) in enumerate(dict) if d["name"] == s), None)
                    people_index2=next((index for (index, d) in enumerate(people) if d["name"] == s), None)
                    print(tom_index)
                    q = dict[tom_index]["quantity"]
                    if int(people[people_index2]["amount"])< q+y:
                        print("ahmed")
                    else:
                        dict[tom_index]["quantity"] = q + y
                        dict[tom_index]["total"] = (q + y) * dict[tom_index]["price"]
                        del_key = "amount"
                        print(dict)
                        #
                        # self.tableWidget_2.setRowCount(len(dict))
                        # row =0
                        # for person in dict :
                        #     self.tableWidget_2.setItem(row,0, QtWidgets.QTableWidgetItem(person["name"]))
                        #     self.tableWidget_2.setItem(row,1, QtWidgets.QTableWidgetItem(str(person["price"])))
                        #     self.tableWidget_2.setItem(row,2, QtWidgets.QTableWidgetItem(str(person["quantity"])))
                        #     self.tableWidget_2.setItem(row,3, QtWidgets.QTableWidgetItem(str(person["total"])))
                        #     row =row+1

                else:
                    print("Ahmed")


            else:
                asd=next((index for (index, d) in enumerate(people) if d["name"] == s), None)
                if int(people[asd]["amount"])< y:
                    print("ahmed")
                else :
                    dict.append(next(x for x in people if x["name"] == s))
                    x = next((index for (index, d) in enumerate(dict) if d["name"] == s), None)
                    dict[x]["quantity"] = y
                    del_key = "amount"
                    dict[x]["total"] = y * dict[x]["price"]
                    print(dict)
                    # self.tableWidget_2.setRowCount(len(dict))
                    # row =0
                    # for person in dict :
                    #     self.tableWidget_2.setItem(row,0, QtWidgets.QTableWidgetItem(person["name"]))
                    #     self.tableWidget_2.setItem(row,1, QtWidgets.QTableWidgetItem(str(person["price"])))
                    #     self.tableWidget_2.setItem(row,2, QtWidgets.QTableWidgetItem(str(person["quantity"])))
                    #     self.tableWidget_2.setItem(row,3, QtWidgets.QTableWidgetItem(str(person["total"])))
                    #     row =row+1






    def loaddata(self):
        people =[{"name":"Dell","price":45,"amount":"50","image":"005.jpg"},{"name":"hp","price":10,"amount":"100","image":"005.jpg"},{"name":"oppo","price":100,"amount":"50","image":"005.jpg"}
        ,{"name":"screen","price":10,"amount":"50","image":"005.jpg"},{"name":"buttery","price":5,"amount":"50","image":"005.jpg"},
        {"name":"DC_charge","price":57,"amount":"50","image":"005.jpg"}
        ]
        self.tableWidget.setRowCount(len(people))
        row =0
        print(people[0]["name"])
        for person in people :
            pic = QtGui.QPixmap(person["image"])
            self.label = QtWidgets.QLabel()
            self.label.setPixmap(pic)
            self.tableWidget.setCellWidget(row,3, self.label)
            self.tableWidget.setItem(row,0, QtWidgets.QTableWidgetItem(str(person["name"])))
            self.tableWidget.setItem(row,1, QtWidgets.QTableWidgetItem(str(person["price"])))
            self.tableWidget.setItem(row,2, QtWidgets.QTableWidgetItem(str(person["amount"])))
            row =row+1
        self.tableWidget.verticalHeader().setDefaultSectionSize(180)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(280)

class purchase(QDialog):
    def __init__(self):
        super(purchase, self).__init__()
        loadUi("main_3.ui",self)
        self.load()
        self.calctotal()
        self.pushButton_5.clicked.connect(self.gotodelete)
        self.pushButton_6.clicked.connect(self.gotoedit)


    def load(self):
        self.tableWidget_2.setRowCount(len(dict))
        row =0
        for person in dict :
            self.tableWidget_2.setItem(row,0, QtWidgets.QTableWidgetItem(person["name"]))
            self.tableWidget_2.setItem(row,1, QtWidgets.QTableWidgetItem(str(person["price"])))
            self.tableWidget_2.setItem(row,2, QtWidgets.QTableWidgetItem(str(person["quantity"])))
            self.tableWidget_2.setItem(row,3, QtWidgets.QTableWidgetItem(str(person["total"])))
            row =row+1



    def calctotal(self):
        total_gold = 0
        for item in dict:
            total_gold += int(item["total"])
        #if int(self.label_11.text()) < total_gold:
            #print("error")
        #else :
            #self.label_12.setText(str(total_gold)+" "+"$")
        self.label_12.setText(str(total_gold)+" "+"$")




    def gotoedit(self):
        people =[{"name":"Dell","price":45,"amount":"50"},{"name":"hp","price":10,"amount":"100"},{"name":"oppo","price":100,"amount":"50"}
        ,{"name":"screen","price":10,"amount":"50"},{"name":"buttery","price":5,"amount":"50"},
        {"name":"DC_charge","price":57,"amount":"50"}
        ]
        c = self.edit.text()
        x =int(self.edit_2.text())
        ss= next((index for (index, d) in enumerate(people) if d["name"] == c), None)
        if int(people[ss]["amount"])<x :
            print("ahmed")
        else :
            for i in range(len(dict)):
                if dict[i]["name"] == c:
                    dict[i]["quantity"]=x
                    dict[i]["total"] = x * dict[i]["price"]
                    break
            self.tableWidget_2.setRowCount(len(dict))
            row =0
            for person in dict :
                self.tableWidget_2.setItem(row,0, QtWidgets.QTableWidgetItem(person["name"]))
                self.tableWidget_2.setItem(row,1, QtWidgets.QTableWidgetItem(str(person["price"])))
                self.tableWidget_2.setItem(row,2, QtWidgets.QTableWidgetItem(str(person["quantity"])))
                self.tableWidget_2.setItem(row,3, QtWidgets.QTableWidgetItem(str(person["total"])))
                row =row+1
            print(dict)
        total_gold = 0
        for item in dict:
            total_gold += int(item["total"])
        self.label_12.setText(str(total_gold)+" "+"$")


    def gotodelete(self):

        z = self.delete_2.text()
        print(z)
        for i in range(len(dict)):
            if dict[i]["name"] == z:
                del dict[i]
                break
        self.tableWidget_2.setRowCount(len(dict))
        row =0
        for person in dict :
            self.tableWidget_2.setItem(row,0, QtWidgets.QTableWidgetItem(person["name"]))
            self.tableWidget_2.setItem(row,1, QtWidgets.QTableWidgetItem(str(person["price"])))
            self.tableWidget_2.setItem(row,2, QtWidgets.QTableWidgetItem(str(person["quantity"])))
            self.tableWidget_2.setItem(row,3, QtWidgets.QTableWidgetItem(str(person["total"])))
            row =row+1
        total_gold = 0
        for item in dict:
            total_gold += int(item["total"])
        self.label_12.setText(str(total_gold)+" "+"$")



# main
app = QApplication(sys.argv)
dict =[]
welcome = cart()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(750)
widget.setFixedWidth(1200)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
