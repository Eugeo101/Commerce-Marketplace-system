class ChangePassword(QDialog):
    def _init_(self):
        super(ChangePassword, self)._init_()
        uic.loadUi("ChangePassword.ui",self)
        self.oldpasswordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.newpasswordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpasswordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm.clicked.connect(self.confirmfunction)
        #self.backbutton.clicked.connect(self.gotoeditacc)


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

            #if (Socket.requestServer(CHANGE_PASSWORD,{PASSWORD:oldpassword})[RESPONSE] == OK):
            #    self.error1.setText("")
            #    ################################return to edit_acc.ui
            #else:
            #    self.error1.setText("Incorrect password")
