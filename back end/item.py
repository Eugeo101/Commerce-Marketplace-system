class Item:
    #constructor
    def __init__(self, ItemID):
        self.ItemID = ItemID

    #setters and getters
    def setName(self, Name):
        self.Name = Name

    def getName(self):
        return self.Name

    def setField(self, field):
        self.field = field

    def getField(self):
        return self.field

    def setProcessor(self, processor):
        self.processor = processor

    def getProcessor(self):
        return self.processor

    def setMemory(self, memory):
        self.memory = memory

    def getMemory(self):
        return self.memory

    def setStorage(self, storage):
        self.storage = storage

    def getStorage(self):
        return self.storage

    def setManfacturer(self, manfacturer):
        self.manfacturer = manfacturer

    def getManfacturer(self):
        return self.manfacturer

    def setPrice(self, price):
        self.price = price

    def getPrice(self):
        return self.price

    def setStock(self, stock):
        self.stock = stock

    def getStock(self):
        return self.stock

    def setPic(self, Pic):
        self.Pic = Pic

    def getPic(self):
        return self.Pic

