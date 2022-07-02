from user import User
from item import Item
import datetime
class Purchases:

    #constructor
    def __int__(self, email, itemID):
        myUser = User(email)
        myItem = Item(itemID)
        self.purchase_id = (email, itemID)

    #operations
    def purchase_item(self):
        pass
        #item_obj = Item()

    def calcPrice(self):
        return self.quantity * self.price

    #setters and getters
    def setQuantity(self, quantity):
        self.quantity = quantity

    def getQuantity(self):
        return self.quantity

    def setDate_Time(self):
        self.Date_Time = (datetime.date, datetime.time)

    def setPrice(self, price):
        self.price = price

    def getPrice(self):
        return self.price

    def setStatus(self, status):
        self.status = status

    def getStatus(self):
        return self.status
