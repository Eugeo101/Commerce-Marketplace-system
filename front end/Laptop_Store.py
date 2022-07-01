import sys
import time
import datetime
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from password_strength import PasswordStats
from password_strength import PasswordPolicy
from email_validator import validate_email, EmailNotValidError
from pyisemail import is_email
from PyQt5.QtCore import *
from pynotifier import Notification
import re
from client import *
from copy import deepcopy


app = QApplication(sys.argv) #app
widget = QtWidgets.QStackedWidget() #stack of screens
cart1=[] #cart
people=[] #items

def gotomain(): #add on stack
    # print('22') #1000
    var = cart()
    widget.addWidget(var)
    widget.setCurrentIndex(widget.currentIndex() + 1)

def showerror(errorCause,details): #error
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle("Error")
    msg.setText(errorCause)
    # msg.setInformativeText("This is additional information")
    msg.setDetailedText(details)
    msg.setStandardButtons(QMessageBox.Ok)
    # msg.buttonClicked.connect(msgbtn)
    msg.exec_()

def notify(title,desc,duration = 3,path='',urg = 'normal'): #notification
    Notification(
        title=title,
        description=desc,
        #icon_path=path,  # On Windows .ico is required, on Linux - .png  EX: '/absolute/path/to/image/icon.png'
        duration=duration,  # Duration in seconds
        urgency=urg
    ).send()

class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi('login.ui', self) #load ui screen
        self.loginbutton.clicked.connect(self.gotomainpage)
        self.passwordin.setEchoMode(QLineEdit.Password)
        self.donthavebutton.clicked.connect(self.gotocreateacc)
        notify('Login Page','Login page is displayed')

    def gotocreateacc(self):
        createacc = createAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotomainpage(self):
        policy = PasswordPolicy.from_names(
            length=10,  # min length: 8
            uppercase=1,  # need min. 2 uppercase letters
            numbers=1,  # need min. 2 digits
            special=1,  # need min. 2 special characters
            nonletters=2,  # need min. 2 non-letter characters (digits, specials, anything)
        )
        email = self.mailin.text()
        password = self.passwordin.text()
        ###print(policy.test(password)) #######imp########

        resp = requestServer(LOGIN, {EMAIL: email, PASSWORD: password})[RESPONSE]

        if not is_email(email,allow_gtld=False):
            showerror('Invalid Email or Password','')
        elif (len(policy.test(password))!=0):
            showerror("Invalid Email or Password",'') #here I just show 'invalid email or password' For Security reasons
        elif(resp == 'Password is incorrect'):
            showerror("Login Failed!", 'check password again')
        elif (resp == 'This Account Doesnt exist'):
            showerror("Login Failed!", 'This account does not exist!')
        else:
            login(email)
            widget.addWidget(cart())
            widget.setCurrentIndex(widget.currentIndex() + 1)

class createAcc(QMainWindow): #back to login page
    def __init__(self):
        super(createAcc, self).__init__()
        uic.loadUi('create_account.ui', self)
        self.backbutton.clicked.connect(self.goback)
        self.signupbutton.clicked.connect(self.gotomainpage)
        self.passin.setEchoMode(QLineEdit.Password)
        self.cpassin.setEchoMode(QLineEdit.Password)
        self.bdatein.setDisplayFormat("yyyy-MM-dd")
        self.bdatein.setMaximumDate(QDate(2015,12,30))
        self.bdatein.setMinimumDate(QDate(1900, 1, 1))
        self.passinfo.setToolTip("Password must \n"
                                 "- be at least 10 characters \n"
                                 "- have at least 1 lowercase character \n"
                                 "- have at least 1 uppercase character \n"
                                 "- have at least 1 special character \n"
                                 "- have at least 1 digit \n")
        self.passinfo.setToolTipDuration(20000)

    def gotomainpage(self):
        policy = PasswordPolicy.from_names(
            length=10,  # min length: 10
            uppercase=1,  # need min. 1 uppercase letters
            numbers=1,  # need min. 1 digits
            special=1,  # need min. 1 special characters
            nonletters=2,  # need min. 2 non-letter characters (digits, specials, anything)
        )
        fname = self.fnamein.text()
        lname = self.lnamein.text()
        email = self.emailin.text()
        password = self.passin.text()
        cpassword = self.cpassin.text()
        bdate = self.bdatein.text() #make its constraints
        city = self.cityin.text()
        country = self.countryin.text()
        job = self.jobin.text()

        if (not fname.isalpha() or not lname.isalpha()):
            showerror("Invalid Name", "Name must be all letters")
        elif not is_email(email,allow_gtld=False):
            showerror('Invalid Email','')
        elif (len(policy.test(password))!=0):
            showerror("Invalid Password", "Password must \n"
                                 "- be at least 10 characters \n"
                                 "- have at least 1 lowercase character \n"
                                 "- have at least 1 uppercase character \n"
                                 "- have at least 1 special character \n"
                                 "- have at least 1 digit \n")
        elif (cpassword!=password):
            showerror("password doesn't match", "")
        elif not country.isalpha():
            showerror("Invalid Country", '')
        elif not city.isalpha():
            showerror("Invalid City", '')
        elif (not job.isalpha()):
            showerror("Invalid Job", '')
        elif(requestServer(CREATE_ACCOUNT, {EMAIL:email, PASSWORD:password, JOB:job, CITY:city,
                                                  COUNTRY:country, LNAME:lname, FNAME:fname, BDATE:bdate})[RESPONSE] == NO):
           showerror("Email Exists Before", 'Try another Email')
        else:
            login(email)
            widget.addWidget(cart())
            widget.setCurrentIndex(widget.currentIndex() + 1)

    def goback(self):
        widget.addWidget(Login())
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def showpassinfo(self):
        showerror('Pass info','must be 10 chars')

class editAccount(QMainWindow): #back to view page
    def __init__(self):
        super(editAccount, self).__init__()
        uic.loadUi('edit_acc.ui', self)
        self.backbutton.clicked.connect(self.goback)
        self.savebutton.clicked.connect(self.gotoviewacc)
        self.chpassbutton.clicked.connect(self.gotochangepass)
        self.bdatein.setDisplayFormat("yyyy-MM-dd")
        self.bdatein.setMaximumDate(QDate(2015, 12, 30))
        self.bdatein.setMinimumDate(QDate(1900, 1, 1))

        # ##print('169')
        data = requestServer1(GET_PROFILE)
        # ##print('171')
        self.mailview.setText(str((getEmail())))
        self.fnamein.setText(str(data[FNAME]))
        self.lnamein.setText(str(data[LNAME]))
        date_str = str(data[BDATE])
        # print(date_str)
        # convert str to QDate
        qdate = QtCore.QDate.fromString(date_str, "yyyy-MM-dd")
        self.bdatein.setDate(qdate)
        # self.bdatein.setText(str(data[BDATE]))
        # # print("182")
        # date = QDateEdit(self)
        # print("184")
        # # setting geometry of the date edit
        # # date.setGeometry(100, 100, 150, 40)
        # print("187")
        # # date
        # listo = data[BDATE].split('-')
        # print(listo)
        # # my_date = datetime.datetime(data[BDATE])
        # # my_date = datetime.datetime.now()
        # print("190")
        # d = QDate(int(listo[0]), int(listo[1]), int(listo[2]))
        # print("192")
        # print(d)
        # # setting date to the date edit
        # date.setDate(d)
        # print("195")
        self.countryin.setText(str(data[COUNTRY]))
        self.cityin.setText(str(data[CITY]))
        self.jobin.setText(str(data[JOB]))
        # ##print('179')

    def gotoviewacc(self):

        fname = self.fnamein.text()
        lname = self.lnamein.text()
        bdate = self.bdatein.text() #make its constraints
        country = self.countryin.text()
        city = self.cityin.text()
        job = self.jobin.text()

        if (not fname.isalpha() or not lname.isalpha()):
            showerror("Invalid Name", "Name must be all letters")
        elif not country.isalpha():
            showerror("Invalid Country", '')
        elif not city.isalpha():
            showerror("Invalid City", '')
        elif (not job.isalpha()):
            showerror("Invalid Job", '')
        elif(requestServer(EDIT_PROFILE, {EMAIL:getEmail(), JOB:job, CITY:city,
                                                   COUNTRY:country, LNAME:lname, FNAME:fname, BDATE:bdate})[RESPONSE] == NO):
            showerror("SOME ERROR OCCURED FROM SERVERSIDE", 'Try another Email')
        else:
            viewacc = viewAccount()
            widget.addWidget(viewacc)
            widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotochangepass(self):
        changepass = ChangePassword()
        widget.addWidget(changepass)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goback(self):
        widget.addWidget(viewAccount())
        widget.setCurrentIndex(widget.currentIndex() + 1)

class viewAccount(QMainWindow): #back button main page
    def __init__(self):
        super(viewAccount, self).__init__()
        uic.loadUi('view_acc.ui', self)
        # print('215')
        self.editbutton.clicked.connect(self.gotoeditaccount)
        data = requestServer1(GET_PROFILE)
        # print('218')
        self.mailview.setText(str(getEmail()))
        # print('224')
        self.fnameview.setText(str(data[FNAME]))
        self.lnameview.setText(str(data[LNAME]))
        # print('227')
        self.bdateview.setText(str(data[BDATE]))
        # print('229')
        self.countryview.setText(str(data[COUNTRY]))
        self.cityview.setText(str(data[CITY]))
        # print('232')
        self.jobview.setText(str(data[JOB]))
        # print('234')
        self.balanceview.setText(str(data[CURRENT_MONEY]))
        #self.showMaximized()
        # print('236') str[
        self.backbutton.clicked.connect(gotomain)

    def gotoeditaccount(self):
        editaccount = editAccount()
        widget.addWidget(editaccount)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        
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
        self.label_12.setText(str(total) + " $")
        self.label_11.setText(str(balance) + " $")
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
        if  total_gold > float(self.label_11.text()[0:-2]):
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
        self.label_12.setText(str(total_gold) + " $")
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
        self.label_12.setText(str(total_gold) + " $")
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
class ChangePassword(QDialog):
    def __init__(self):
        super(ChangePassword, self).__init__()
        uic.loadUi("ChangePassword.ui",self)
        self.oldpasswordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.newpasswordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpasswordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm.clicked.connect(self.confirmfunction)
        self.backbutton.clicked.connect(self.goback)


    def confirmfunction(self):
        newpassword = self.newpasswordfield.text()
        oldpassword = self.oldpasswordfield.text()
        confirmpassword = self.confirmpasswordfield.text()
        uppercase = False
        lowercase = False
        numeric = False
        specialchar = False


        if len(newpassword)==0 or len(oldpassword)==0 or len(confirmpassword)==0:
            self.error4.setText("Please input all fields.")

        else:
            self.error4.setText("")

            special_char = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

            if (special_char.search(newpassword) == None):
                specialchar = False
            else:
                specialchar = True
            for i in range(0, len(newpassword)):
                if newpassword[i].isupper():
                    uppercase = True
                if newpassword[i].islower():
                    lowercase = True
                if newpassword[i].isnumeric():
                    numeric = True

            if len(newpassword) >= 10 and uppercase == True and lowercase == True and numeric == True and specialchar == True:
                self.error2.setText("")
                if newpassword == confirmpassword:
                    self.error3.setText("")
                else:
                    self.error3.setText("Must match the previuos entry")
            else:
                self.error2.setText(
                    "The password must be at least 10 characters contains uppercase, lowercase, numbers and special characters")
            ##print('290')
            result = requestServer(CHANGE_PASSWORD,{PASSWORD:oldpassword, NEW_PASSWORD: newpassword})
            ##print('291')
            if (result[RESPONSE] == OK):
               # self.error1.setText("")
               self.goback()
            else:
               self.error1.setText("Incorrect password")

    def goback(self):
        ##print('300')
        widget.addWidget(editAccount())
        widget.setCurrentIndex(widget.currentIndex() + 1)
        
class Deposit(QDialog):

    balance = 0

    def __init__(self):
        super(Deposit, self).__init__()
        uic.loadUi("Deposit.ui",self)
        self.confirmDeposit.clicked.connect(self.depositfunction)
        self.balance = str(requestServer1(GET_BALANCE)[CASH])
        self.balanceview.setText(self.balance)
        # self.depositfield.textChanged.connect(self.changenewbalance)
        self.backbutton.clicked.connect(gotomain)

    # def changenewbalance(self):
    #     try:
    #         depositamount = self.depositfield.text()
    #         # ##print(depositamount)
    #         depamountint = int(depositamount)
    #         balanceint = int(self.balance)
    #         self.balance = depamountint + balanceint # 600 ->
    #         self.newBalance.setText(str(self.balance))
    #         self.newBalance.repaint()
    #     except:
    #         self.newBalance.setText(str(self.balance))


    def depositfunction(self):
        depositamount = self.depositfield.text()
        numeric = True

        for i in range(0,len(depositamount)):
            numeric = numeric & depositamount[i].isnumeric()

        if numeric == False or len(depositamount) == 0:
            self.depositerror.setText("Please Enter Numbers")
        else:
            # self.depositerror.setText("")
            newbalance = requestServer(DEPOSIT, {DEPOSIT_AMOUNT: depositamount})[CASH]
            gotomain()       

mainwindow = Login()
widget.addWidget(mainwindow)
widget.setFixedHeight(850)
widget.setFixedWidth(1200)
widget.setWindowTitle("Laptop Store")
widget.setWindowIcon(QtGui.QIcon("logo.png"))
# setWindowIcon(QtGui.QIcon('logo.png'))
# setWindowTitle("Laptop Store")
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")
