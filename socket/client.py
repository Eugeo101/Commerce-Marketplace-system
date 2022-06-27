import re
import socket
import json
from collections import namedtuple
from json import JSONEncoder
from urllib import request

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.13"
ADDR = (SERVER, PORT)

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
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

class Socket:
    __email = ""
    def __init__(self,email):
        self.__email = email
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
    def requestServer(requestType,message):
        if requestType == CREATE_ACCOUNT:
            message["request"] = CREATE_ACCOUNT
            Socket.__send(message)
            #{"respone":"OK"} -> successful creation of account / {"respone":"NO"} -> account already exists
        elif requestType == EDIT_PROFILE:
            message["request"] = EDIT_PROFILE
            Socket.__send(message)
            #{"respone":"OK"} -> successful creation of account / {"respone":"NO"} -> email already exists
        elif requestType == GET_PROFILE:
            message["email"] = Socket.__email
            message["request"] = GET_PROFILE
            Socket.__send(message)
            #{"fname":"Ahmed","lname":"Alaa","email":"Ahmed@gmail.com","bdate":"2000\01\01","country":"Egypt","city":"Cairo","job":"Worker","cash":"3000"}
        elif requestType == LOGIN:
            message["request"] = LOGIN
            Socket.__send(message)
            #{"respone":"OK"} -> succesful login / {"respone":"NO"} -> invalid email or password
        elif requestType == CHANGE_PASSWORD:
            message["email"] = Socket.__email
            message["request"] = CHANGE_PASSWORD
            Socket.__send(message)
            #{"response":"OK"} -> acknoweldge
        elif requestType == DEPOSIT:
            message["email"] = Socket.__email
            message["request"] = DEPOSIT
            Socket.__send(message)
            #{"balance":"3500"}
        elif requestType == BUY:
            message["email"] = Socket.__email
            message["request"] = BUY
            Socket.__send(message)
            #{"response":"OK","balance":"3000"} -> successful buy / {"response":"NO","items":[]}  -> not enough in stock
        elif requestType == ADD_CART:
            message["email"] = Socket.__email
            message["request"] = ADD_CART
            Socket.__send(message)
            #{"response":"OK"} -> successfuly added to cart / {"response":"NO","stock":"3"} -> not enough in stock
        elif requestType == REMOVE_CART:
            message["email"] = Socket.__email
            message["request"] = REMOVE_CART
            Socket.__send(message)
            #{"response":"OK"} -> successful removal
        elif requestType == GET_CART:
            message["email"] = Socket.__email
            message["request"] = GET_CART
            Socket.__send(message)
            #
        elif requestType == GET_BALANCE:
            message["email"] = Socket.__email
            message["request"] = GET_BALANCE
            Socket.__send(message)
            #{"balance":"3500"}
        elif requestType == GET_ITEMS:
            get_items = {"request":"GET_ITEMS"}
            Socket.__send(get_items)
            #{"items":[]}
        return Socket.__receive()


# login = {"email":"Ahmed@gmail.com","password":"Ahmed50"}
# change_password = {"email":"Ahmed@gmail.com","password":"Ahmed50","new_password":"Ahmed40"}
# deposit = {"email":"Ahmed@gmail.com","amount":"500"}
# cart = {"email":"Ahmed@gmail.com","item":"30"}
# get_request = {"email":"Ahmed@gmail.com"}
# account_info = {"fname":"Ahmed","lname":"Alaa","email":"Ahmed@gmail.com","password":"Ahmed50","bdate":"2000\01\01","country":"Egypt","city":"Cairo","job":"Worker"}
# edit_info = {"fname":"Ahmed","lname":"Alaa","email":"Ahmed@gmail.com","bdate":"2000\01\01","country":"Egypt","city":"Cairo","Job":"Worker"}
# profile = {"fname":"Ahmed","lname":"Alaa","email":"Ahmed@gmail.com","bdate":"2000\01\01","country":"Egypt","city":"Cairo","Job":"Worker","cash":"3000"}

