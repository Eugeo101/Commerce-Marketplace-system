
import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from password_strength import PasswordStats
from password_strength import PasswordPolicy
from email_validator import validate_email, EmailNotValidError
from pyisemail import is_email
from PyQt5.QtCore import *
from pynotifier import Notification
from client import *

app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()

def gotomain(): #add on stack
    # print('22') #1000
    var = cart()
    widget.addWidget(var)
    widget.setCurrentIndex(widget.currentIndex() + 1)

def showerror(errorCause,details):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle("Error")
    msg.setText(errorCause)
    # msg.setInformativeText("This is additional information")
    msg.setDetailedText(details)
    msg.setStandardButtons(QMessageBox.Ok)
    # msg.buttonClicked.connect(msgbtn)
    msg.exec_()

def notify(title,desc,duration = 10,path='',urg = 'normal'):
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

mainwindow = Login()
widget.addWidget(mainwindow)
widget.setFixedHeight(600)
widget.setFixedWidth(800)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")