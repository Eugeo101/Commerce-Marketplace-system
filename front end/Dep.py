class Deposit(QDialog):

    balance = 0

    def _init_(self):
        super(Deposit, self)._init_()
        uic.loadUi("Deposit.ui",self)
        self.confirmDeposit.clicked.connect(self.depositfunction)
        self.balance = '1' ##delete
        #balance = Socket.requestServer(GET_BALANCE)[CASH]
        #int(balance) = int(balance)
        #self.balance.setText(balance)
        self.balanceview.setText("1") ##delete
        self.depositfield.textChanged.connect(self.changenewbalance)
        #self.backbutton.clicked.connect(self.gotomainscreen)

    def changenewbalance(self):
        try:
            depositamount = self.depositfield.text()
            depamountint = int(str(depositamount))
            balanceint = int(self.balance)
            #fstring = depamountint + balanceint
            self.newBalance.setText(str(depamountint + balanceint))
        except:
            self.newBalance.setText(str(self.balance))

    def depositfunction(self):
        depositamount = self.depositfield.text()
        numeric = True

        #if(not depositamount.isdigit()):

        for i in range(0,len(depositamount)):
            numeric = numeric & depositamount[i].isnumeric()

        if numeric == False:
            self.depositerror.setText("Please Enter Numbers Only")
        else:
            self.depositerror.setText("")
        #    newbalance = Socket.requestServer(DEPOSIT, {DEPOSIT_AMOUNT: depositamount})[CASH]
            ##################same back function
