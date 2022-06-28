import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from password_strength import PasswordStats
from password_strength import PasswordPolicy
from email_validator import validate_email, EmailNotValidError
from pyisemail import is_email
#from client import *

app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()

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

class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi('login.ui', self)
        self.loginbutton.clicked.connect(self.gotomainpage)
        self.passwordin.setEchoMode(QLineEdit.Password)
        self.donthavebutton.clicked.connect(self.gotocreateacc)

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
        self.signupbutton.clicked.connect(self.gotomainpage)
        self.passin.setEchoMode(QLineEdit.Password)
        self.cpassin.setEchoMode(QLineEdit.Password)

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

        if not is_email(email,allow_gtld=False):
            showerror('Invalid Email','')
        elif (not job.isalpha()):
            showerror("Invalid Job", '')
        elif not country.isalpha():
            showerror("Invalid Country", '')
        elif not city.isalpha():
            showerror("Invalid City", '')
        elif (len(policy.test(password))!=0):
            showerror("Invalid Password", "Password length must be 10 min and at least contains 1 upper case letter 1 digit and 1 special char")
        elif (cpassword!=password):
            showerror("password doesn't match", "")
        elif (not fname.isalpha() or not lname.isalpha()):
            showerror("Invalid Name", "Name must be all letters")
        #elif(Socket.requestServer(CREATE_ACCOUNT, {EMAIL:email, PASSWORD:password, JOB:job, CITY:city,
         #                                          COUNTRY:country, LNAME:lname, FNAME:fname, BDATE:bdate})[RESPONSE] == NO):
          #  showerror("Email Exists Before", 'Try another Email')
        else:
            #Socket.login(email)
            widget.addWidget(mainpage)
            widget.setCurrentIndex(widget.currentIndex() + 1)

class editAccount(QMainWindow): #back to view page
    def __init__(self):
        super(editAccount, self).__init__()
        uic.loadUi('edit_acc.ui', self)
        self.savebutton.clicked.connect(self.gotoviewacc)
        self.chpassbutton.clicked.connect(self.gotochangepass)
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
        ############################## Dont forget BDAAAAAAATEEEEEEEE
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

mainwindow = viewAccount()
widget.addWidget(mainwindow)
widget.setFixedHeight(600)
widget.setFixedWidth(800)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")