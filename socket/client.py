import re
import socket
import json
from collections import namedtuple
from json import JSONEncoder
from urllib import request

#---------requestType----------#
CREATE_ACCOUNT = "CREATE_ACCOUNT"
LOGIN = "LOGIN"
EDIT_PROFILE = "EDIT_PROFILE"
CHANGE_PASSWORD = "CHANGE_PASSWORD"
DEPOSIT = "DEPOSIT"
BUY = "BUY"
GET_BALANCE = "GET_BALANCE"
GET_ITEMS = "GET_ITEMS"
GET_PROFILE = "GET_PROFILE"
ADD_CART = "ADD_CART"
REMOVE_CART = "REMOVE_CART"
GET_CART = "GET_CART"
REQUEST = "request"
#-----------------------------#

#-----------Response from server-------------#
RESPONSE = "response"
FNAME = "fname"
LNAME = "lname"
EMAIL = "email"
BDATE = "bdate"
COUNTRY = "country"
CITY = "city"
JOB = "job"
CASH = "cash"
STOCK = "stock"
ITEMS = "items"
PASSWORD = "password"
NEW_PASSWORD = "new_password"
DEPOSIT_AMOUNT = "amount"
ITEM_ID = "item_id"
OK = "OK"
NO = "NO"
#--------------------------------------------#

#------------Initialize client socket-----------#
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
SERVER = "192.168.1.13"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
#-----------------------------------------------#

class Socket:
    __email = "user@email.com"

    def __customDecoder(Dict):
        return namedtuple('X', Dict.keys())(*Dict.values())

    def __send(msg):
        message = json.dumps(msg)
        print("Message Sent:" + msg)
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)

    def __receive():
        msg_length = client.recv(HEADER).decode(FORMAT)
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)
        print("Message Received:" + msg)
        return json.loads(msg, object_hook=Socket.__customDecoder)

    @staticmethod
    def login(email):
        Socket.__email = email

    @staticmethod
    def getEmail():
        return Socket.__email

    @staticmethod
    def requestServer(requestType,message):
        message[REQUEST] = requestType
        if requestType == CHANGE_PASSWORD or requestType == DEPOSIT or requestType == ADD_CART or requestType == REMOVE_CART:
            message[EMAIL] = Socket.__email
        Socket.__send(message)
        return Socket.__receive()
    @staticmethod
    def requestServer(requestType):
        message = {REQUEST:requestType}
        if requestType != GET_ITEMS:
            message[EMAIL] = Socket.__email
        Socket.__send(message)
        return Socket.__receive()


# if requestType == CREATE_ACCOUNT:
#     #{"respone":"OK"} -> successful creation of account / {"respone":"NO"} -> account already exists
# elif requestType == EDIT_PROFILE:
#     #{"respone":"OK"} -> successful creation of account / {"respone":"NO"} -> email already exists
# elif requestType == LOGIN:
#     #{"respone":"OK"} -> succesful login / {"respone":"NO"} -> invalid email or password
# elif requestType == CHANGE_PASSWORD:
#     message[EMAIL] = Socket.__email
#     #{"response":"OK"} -> acknoweldge
# elif requestType == DEPOSIT:
#     message[EMAIL] = Socket.__email
#     #{"cash":"3500"}
# elif requestType == ADD_CART:
#     message[EMAIL] = Socket.__email
#     #{"response":"OK"} -> successfuly added to cart / {"response":"NO","stock":"3"} -> not enough in stock
# elif requestType == REMOVE_CART:
#     message[EMAIL] = Socket.__email
#     #{"response":"OK"} -> successful removal

# if requestType == GET_PROFILE:
#     #{"fname":"Ahmed","lname":"Alaa","email":"Ahmed@gmail.com","bdate":"2000\01\01","country":"Egypt","city":"Cairo","job":"Worker","cash":"3000"}
# elif requestType == BUY:
#     #{"response":"OK","cash":"3000"} -> successful buy / {"response":"NO","items":[]}  -> not enough in stock
# elif requestType == GET_CART:
#     #{"items":[]}
# elif requestType == GET_BALANCE:
#     #{"cash":"3500"}
# elif requestType == GET_ITEMS:
#     #{"items":[]}
# login = {"email":"Ahmed@gmail.com","password":"Ahmed50"}
# change_password = {"email":"Ahmed@gmail.com","password":"Ahmed50","new_password":"Ahmed40"}
# deposit = {"email":"Ahmed@gmail.com","amount":"500"}
# cart = {"email":"Ahmed@gmail.com","item_id":"30"}
# get_request = {"email":"Ahmed@gmail.com"}
# account_info = {"fname":"Ahmed","lname":"Alaa","email":"Ahmed@gmail.com","password":"Ahmed50","bdate":"2000\01\01","country":"Egypt","city":"Cairo","job":"Worker"}
# edit_info = {"fname":"Ahmed","lname":"Alaa","email":"Ahmed@gmail.com","bdate":"2000\01\01","country":"Egypt","city":"Cairo","Job":"Worker"}
# profile = {"fname":"Ahmed","lname":"Alaa","email":"Ahmed@gmail.com","bdate":"2000\01\01","country":"Egypt","city":"Cairo","Job":"Worker","cash":"3000"}

