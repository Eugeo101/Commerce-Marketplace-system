import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from password_strength import PasswordStats
from password_strength import PasswordPolicy
from email_validator import validate_email, EmailNotValidError
from pyisemail import is_email
#from client import *
from PyQt5.QtCore import *
from pynotifier import Notification


app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()

#def isvalid(bdate):
#    if(len(bdate) != 10):
#        return 0
#    if(bdate[0].isdigit() and bdate[1].isdigit()
#            and bdate[2].isdigit() and bdate[3].isdigit() and bdate[5].isdigit()
 #           and bdate[6].isdigit() and bdate[8].isdigit() and bdate[9].isdigit()
  #          and (bdate[0] == 1 or bdate[0] == 2) and bdate[4] == '-'
   #         and bdate[7] == '-' ):
    #    return 1
    #return 0


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
        icon_path=path,  # On Windows .ico is required, on Linux - .png  EX: '/absolute/path/to/image/icon.png'
        duration=duration,  # Duration in seconds
        urgency=urg
    ).send()

class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi('login.ui', self)
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
        mainpage = mainPage()
        email = self.mailin.text()
        password = self.passwordin.text()
        #print(policy.test(password)) #######imp########

        if not is_email(email,allow_gtld=False):
            showerror('Invalid Email or Password','')
        elif (len(policy.test(password))!=0):
            showerror("Invalid Email or Password",'') #here I just show 'invalid email or password' For Security reasons
        #elif(Socket.requestServer(LOGIN, {EMAIL:email, PASSWORD:password})[RESPONSE] == NO):
        #    showerror("Invalid Email or Password", '')
        else:
        #    Socket.login(email)
            widget.addWidget(mainpage)
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
        #self.passinfo.setEnabled()
        #self.passinfo.setMouseTracking()
        #self.passinfo.mouseMoveEvent()

    def gotomainpage(self):
        policy = PasswordPolicy.from_names(
            length=10,  # min length: 10
            uppercase=1,  # need min. 1 uppercase letters
            numbers=1,  # need min. 1 digits
            special=1,  # need min. 1 special characters
            nonletters=2,  # need min. 2 non-letter characters (digits, specials, anything)
        )
        mainpage = mainPage()
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
            showerror("Invalid Password", "Password length must be 10 min and at least contains 1 upper case letter 1 digit and 1 special char")
        elif (cpassword!=password):
            showerror("password doesn't match", "")
        elif not country.isalpha():
            showerror("Invalid Country", '')
        elif not city.isalpha():
            showerror("Invalid City", '')
        elif (not job.isalpha()):
            showerror("Invalid Job", '')
        #elif(Socket.requestServer(CREATE_ACCOUNT, {EMAIL:email, PASSWORD:password, JOB:job, CITY:city,
         #                                          COUNTRY:country, LNAME:lname, FNAME:fname, BDATE:bdate})[RESPONSE] == NO):
          #  showerror("Email Exists Before", 'Try another Email')
        else:
            #Socket.login(email)
            widget.addWidget(mainpage)
            widget.setCurrentIndex(widget.currentIndex() + 1)

    def goback(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        dwidget = widget(widget.currentIndex() + 1)
        widget.removeWidget(dwidget)

class editAccount(QMainWindow): #back to view page
    def __init__(self):
        super(editAccount, self).__init__()
        uic.loadUi('edit_acc.ui', self)
        self.savebutton.clicked.connect(self.gotoviewacc)
        self.chpassbutton.clicked.connect(self.gotochangepass)
        self.bdatein.setDisplayFormat("yyyy-MM-dd")
        self.bdatein.setMaximumDate(QDate(2015, 12, 30))
        self.bdatein.setMinimumDate(QDate(1900, 1, 1))

        #data = Socket.requestServer(GET_PROFILE)
        #self.mailview.setText(Socket.getEmail())
        #self.fnamein.setText(data[FNAME])
        #self.lnamein.setText(data[LNAME])
        #self.bdatein.setText(data[BDATE])
        #self.countryin.setText(data[COUNTRY])
        #self.cityin.setText(data[CITY])
        #self.jobin.setText(data[JOB])

    def gotoviewacc(self):
        viewacc = viewAccount()
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
        #elif(Socket.requestServer(EDIT_PROFILE, {EMAIL:Socket.getEmail(), JOB:job, CITY:city,
        #                                           COUNTRY:country, LNAME:lname, FNAME:fname, BDATE:bdate})[RESPONSE] == NO):
        #    showerror("SOME ERROR OCCURED FROM SERVERSIDE", 'Try another Email')
        else:
            widget.addWidget(viewacc)
            widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotochangepass(self):
        changepass = changePass()
        widget.addWidget(changepass)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class mainPage(QMainWindow):
    def __init__(self):
        super(mainPage, self).__init__()
        uic.loadUi('mainpage.ui', self)

class changePass(QMainWindow):
    def __init__(self):
        super(changePass, self).__init__()
        uic.loadUi('change_pass.ui', self)

class viewAccount(QMainWindow): #back button main page
    def __init__(self):
        super(viewAccount, self).__init__()
        uic.loadUi('view_acc.ui', self)
        self.editbutton.clicked.connect(self.gotoeditaccount)
        #data = Socket.requestServer(GET_PROFILE)
        #self.mailview.setText(Socket.getEmail())
        #self.fnameview.setText(data[FNAME])
        #self.lnameview.setText(data[LNAME])
        #self.bdateview.setText(data[BDATE])
        #self.countryview.setText(data[COUNTRY])
        #self.cityview.setText(data[CITY])
        #self.jobview.setText(data[JOB])
        #self.balanceview.setText(data[CASH])

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