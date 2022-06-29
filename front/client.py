import re
import socket
import pickle
import os
import json
from collections import namedtuple
from json import JSONEncoder
from urllib import request

#---------requestType----------#
REQUEST = "request"
CREATE_ACCOUNT = "CREATE_ACCOUNT"
LOGIN = "LOGIN"
EDIT_PROFILE = "EDIT_PROFILE"
CHANGE_PASSWORD = "CHANGE_PASSWORD"
DEPOSIT = "DEPOSIT"
BUY = "PURCHASE"
GET_BALANCE = "GET_BALANCE"
GET_ITEMS = "GET_ITEMS"
GET_PROFILE = "GET_PROFILE"
ADD_CART = "ADD_ITEM"
REMOVE_CART = "REMOVE_ITEM"
GET_CART = "GET_CART"
HISTORY = "HISTORY"
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
ITEM_NAME = "name"
DESCRIPTION  = "description"
QUANTITY = "quantity"
OK = "OK"
NO = "NO"
INCORRECT_PASSWORD = "Password is incorrect"
INCORRECT_EMAIL = "This Account Doesnt exist"
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

    def __write_file(data, filename):
        # Convert binary data to proper format and write it on Hard Disk
        file = open(filename, 'wb')
        file.write(data)

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
        if msg_length:
            msg_length = int(msg_length)
            msg = client.recv(msg_length)
            try:
                message = msg.decode(FORMAT)
                message = json.loads(message, object_hook=Socket.__customDecoder) #json -> dicto
            except:
                message = pickle.loads(message)  # json -> dicto
                directory = "assests"
                parent_dir = os.getcwd()
                path = os.path.join(parent_dir, directory)
                if (os.path.exists(path) == False):
                    # create folder
                    os.mkdir(path)
                # mapping bytes -> name
                caption = 'Image'
                # print(response_msg)
                if (message['msg'] == 'cart'):
                    caption = 'Cart'
                elif (message['msg'] == 'img'):
                    caption = 'Image'
                for i in range(len(message[ITEMS])):
                    Socket.__write_file(message[ITEMS][i][2],f"{path}\\" + caption + str(i) + ".jpeg")
                    message[ITEMS][i] = list(message[ITEMS][i])
                    message[ITEMS][i][2] = caption + str(i) + ".jpeg"
                    message[ITEMS][i] = tuple(message[ITEMS][i])
            print("Message Received:" + message)
            return message

    @staticmethod
    def login(email):
        Socket.__email = email

    @staticmethod
    def getEmail():
        return Socket.__email

    @staticmethod
    def requestServer(requestType,message):
        message[REQUEST] = requestType
        if requestType == GET_PROFILE or requestType == CHANGE_PASSWORD or requestType == DEPOSIT or requestType == ADD_CART or requestType == REMOVE_CART or requestType == GET_CART or requestType == GET_BALANCE or requestType == HISTORY:
            message[EMAIL] = Socket.__email
        Socket.__send(message)
        return Socket.__receive()
    @staticmethod
    def requestServer(requestType):
        message = {}
        return Socket.requestServer(requestType,message)


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
