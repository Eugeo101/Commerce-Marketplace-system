import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5.QtGui import QPixmap
import re
import sqlite3
#from client import *



class Deposit(QDialog):
    def __init__(self):
        super(Deposit, self).__init__()
        loadUi("Deposit.ui",self)
        self.confirmDeposit.clicked.connect(self.depositfunction)
        #self.cancelDeposit.clicked.connect(self.go to main screen)
        self.showBalance.clicked.connect(self.getbalance)



    def depositfunction(self):

        depositamount = self.depositfield.text()
        numeric = True

        for i in range(0,len(depositamount)):
            numeric = numeric & depositamount[i].isnumeric()

        if numeric == False:
            self.depositerror.setText("Please Enter Numbers Only")
        else:
            self.depositerror.setText("")
            user = self.usernamefield.text()
            conn = sqlite3.connect("test.db")
            cur = conn.cursor()
            query = 'SELECT balance FROM UserBalance WHERE username =\''+user+"\'"
            cur.execute(query)
            currentBalance = cur.fetchone()[0]
            new = currentBalance + float(depositamount)
            self.newBalance.setText(str(new) +'$')
            query = f"UPDATE UserBalance SET balance = '{new}' WHERE username = '{user}'"
            cur.execute(query)
            conn.commit()
            conn.close()
            print('The balance is succesfully changed')


    def getbalance(self):
        self.newBalance.setText("")
        user = self.usernamefield.text()
        conn = sqlite3.connect("test.db")
        cur = conn.cursor()
        query = 'SELECT balance FROM UserBalance WHERE username =\''+user+"\'"
        cur.execute(query)
        currentBalance = cur.fetchone()[0]
        self.balance.setText(str(currentBalance) + '$')



#################################################################
#################################################################


# main
app = QApplication(sys.argv)
d = Deposit()
widget = QtWidgets.QStackedWidget()
widget.addWidget(d)
widget.setFixedHeight(561)
widget.setFixedWidth(761)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
