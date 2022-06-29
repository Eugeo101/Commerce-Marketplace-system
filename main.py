import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5.QtGui import QPixmap
import re
import sqlite3
#from client import *



class ChangePassword(QDialog):
    def __init__(self):
        super(ChangePassword, self).__init__()
        loadUi("ChangePassword.ui",self)
        self.oldpasswordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.newpasswordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpasswordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm.clicked.connect(self.confirmfunction)
        #self.cancel.clicked.connect(self.gotologin)


    def confirmfunction(self):
        user = self.usernamefield.text()
        newpassword = self.newpasswordfield.text()
        oldpassword = self.oldpasswordfield.text()
        confirmpassword = self.confirmpasswordfield.text()
        uppercase = False
        lowercase = False
        numeric = False
        specialchar = False


        if len(user)==0 and  len(newpassword)==0 or len(oldpassword)==0 or len(confirmpassword)==0:
            self.error4.setText("Please input all fields.")

        else:
            self.error4.setText("")
                   #get user
            conn = sqlite3.connect("shop_data.db")
            cur = conn.cursor()
            query = 'SELECT password FROM login_info WHERE username =\''+user+"\'"
            cur.execute(query)
            result_pass = cur.fetchone()[0]

            #if Socket.requestServer(CHANGE_PASSWORD,{PASSWORD:oldpassword})[RESPONSE] == OK
            if result_pass == oldpassword:
                self.error1.setText("")
                special_char = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
                if(special_char.search(newpassword) == None):
                    specialchar = False
                else:
                    specialchar = True
                for i in range(0,len(newpassword)):
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
                        query = f"UPDATE login_info SET password = '{newpassword}' WHERE username = '{user}'"
                        cur.execute(query)
                        conn.commit()
                        conn.close()
                        print('password is succesfully changed')



                    else:
                        self.error3.setText("Must match the previuos entry")
                else:
                    self.error2.setText("The password must be at least 10 characters contains uppercase, lowercase, numbers and special characters")

            else:
                self.error1.setText("Incorrect password")





# main
app = QApplication(sys.argv)
change = ChangePassword()
widget = QtWidgets.QStackedWidget()
widget.addWidget(change)
widget.setFixedHeight(561)
widget.setFixedWidth(761)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
