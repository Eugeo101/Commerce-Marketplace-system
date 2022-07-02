import re
import socket
import pickle
import os
import json
from collections import namedtuple
from json import JSONEncoder
from urllib import request

# ---------requestType----------#
REQUEST = "request"
CREATE_ACCOUNT = "CREATE_ACCOUNT"
LOGIN = "LOGIN"
EDIT_PROFILE = "EDIT_PROFILE"
CHANGE_PASSWORD = "CHANGE_PASSWORD"
DEPOSIT = "DEPOSIT"
BUY = "PURCHASE"
PURCHASE = "BUY_ALL"
GET_BALANCE = "GET_BALANCE"
GET_ITEMS = "GET_ITEMS"
GET_PROFILE = "GET_PROFILE"
ADD_CART = "ADD_ITEM"
REMOVE_CART = "REMOVE_ITEM"
GET_CART = "GET_CART"
HISTORY = "HISTORY"
# -----------------------------#

# -----------Response from server-------------#
RESPONSE = "response"
FNAME = "fname"
LNAME = "lname"
EMAIL = "email"
BDATE = "bdate"
COUNTRY = "country"
CITY = "city"
JOB = "job"
CASH = "balance"
CURRENT_MONEY = 'cash'
STOCK = "stock"
ITEMS = "items"
PASSWORD = "password"
NEW_PASSWORD = "new_password"
DEPOSIT_AMOUNT = "amount"
ITEM_NAME = "name"
DESCRIPTION = "description"
QUANTITY = "quantity"
OK = "OK"
NO = "NO"
INCORRECT_PASSWORD = "Password is incorrect"
INCORRECT_EMAIL = "This Account Doesnt exist"
IMAGE = "Image"
PROCESSOR = "processor"
MEMORY = "memory"
STORAGE = "storage"
MANUFACT = "manufact"
PRICE = "price"
# --------------------------------------------#

# ------------Initialize client socket-----------#
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
SERVER = "192.168.1.5"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
# -----------------------------------------------#

# class Socket:
#     email = "user@email.com"

def customDecoder(Dict): #dict to tuple?
    return namedtuple('X', Dict.keys())(*Dict.values())

def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    file = open(filename, 'wb')
    file.write(data)

def send(msg):
    message = json.dumps(msg)
    print("Message Sent:" + message)
    message = message.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def receive():
    # print('93')
    response_length = client.recv(HEADER).decode(FORMAT)  # '4'
    # print('95')
    if response_length:
        response_length = int(response_length)  # 4
        response_msg = client.recv(response_length)
        try:
            # print('100')
            response_msg_json = response_msg.decode(FORMAT)  # json
            response_msg_json = json.loads(response_msg_json)  # json -> dicto
            print(f"[SERVER RESPONSE] {response_msg_json}")  # some number of bytes
            return response_msg_json
        except:
            # print('106')
            response_msg = pickle.loads(response_msg)  # json -> dicto
            # print(response_msg)
            directory = "assests"
            parent_dir = os.getcwd()
            path = os.path.join(parent_dir, directory)
            if (os.path.exists(path) == False):
                # create folder
                os.mkdir(path)

            # mapping bytes -> name
            caption = 'Image'
            if (response_msg['msg'] == 'cart'):
                caption = 'Cart'
            elif (response_msg['msg'] == 'img'):
                caption = 'Image'
            for i in range(len(response_msg['items'])):
                write_file(response_msg['items'][i][2],
                           f"{path}\\" + caption + str(i) + ".jpeg")
                response_msg['items'][i] = list(response_msg['items'][i])
                response_msg['items'][i][2] = caption + str(i) + ".jpeg"
                response_msg['items'][i] = tuple(response_msg['items'][i])
            print(f"[SERVER RESPONSE] {response_msg}")  # some number of bytes
            return response_msg

# def receive(self):
#     msg_length = client.recv(HEADER).decode(FORMAT)
#     if msg_length:
#         msg_length = int(msg_length)
#         msg = client.recv(msg_length)
#         print("Msg Received1:" + msg)
#         try:
#             message = msg.decode(FORMAT)
#             message = json.loads(message, object_hook=Socket.customDecoder)  # json -> dicto
#         except:
#             message = pickle.loads(message)  # json -> dicto
#             directory = "assests"
#             parent_dir = os.getcwd()
#             path = os.path.join(parent_dir, directory)
#             if (os.path.exists(path) == False):
#                 # create folder
#                 os.mkdir(path)
#             # mapping bytes -> name
#             caption = 'Image'
#             # print(response_msg)
#             if (message['msg'] == 'cart'):
#                 caption = 'Cart'
#             elif (message['msg'] == 'img'):
#                 caption = 'Image'
#             for i in range(len(message[ITEMS])):
#                 Socket.write_file(message[ITEMS][i][2], f"{path}\\" + caption + str(i) + ".jpeg")
#                 message[ITEMS][i] = list(message[ITEMS][i])
#                 message[ITEMS][i][2] = caption + str(i) + ".jpeg"
#                 message[ITEMS][i] = tuple(message[ITEMS][i])
#         print("Message Received:" + message)
#         return message

email = ""
# @staticmethod
def login(my_email):
    global email
    email = my_email

# @staticmethod
def getEmail():
    return email

# @staticmethod
def requestServer(requestType, message):
    # print('173')
    if (requestType == PURCHASE):
        for buyRequest in message[ITEMS]: #for loop for each purchase
            requestServer(BUY, {ITEM_NAME: buyRequest[ITEM_NAME], DESCRIPTION: buyRequest[DESCRIPTION], QUANTITY: buyRequest[QUANTITY]})
    else:
        message[REQUEST] = requestType
        if requestType == GET_PROFILE or requestType == CHANGE_PASSWORD or requestType == DEPOSIT or requestType == ADD_CART or requestType == REMOVE_CART or requestType == GET_CART or requestType == GET_BALANCE or requestType == HISTORY or requestType == BUY or requestType == GET_ITEMS:
            message[EMAIL] = email
        send(message)

    result = receive()
    return result

# @staticmethod
def requestServer1(requestType):
    # print('188')
    message = {}
    if (requestType == PURCHASE):
        for buyRequest in message[ITEMS]: #for loop for each purchase
            requestServer(BUY, {ITEM_NAME: buyRequest[ITEM_NAME], DESCRIPTION: buyRequest[DESCRIPTION], QUANTITY: buyRequest[QUANTITY]})
    else:
        message[REQUEST] = requestType
        if requestType == GET_PROFILE or requestType == CHANGE_PASSWORD or requestType == DEPOSIT or requestType == ADD_CART or requestType == REMOVE_CART or requestType == GET_CART or requestType == GET_BALANCE or requestType == HISTORY or requestType == BUY or requestType == GET_ITEMS:
            message[EMAIL] = email
        send(message)
    # print('198')
    result = receive()
    # print(result)
    return result

# if requestType == CREATE_ACCOUNT:
#     #{"respone":"OK"} -> successful creation of account / {"respone":"NO"} -> account already exists
# elif requestType == EDIT_PROFILE:
#     #{"respone":"OK"} -> successful creation of account / {"respone":"NO"} -> email already exists
# elif requestType == LOGIN:
#     #{"respone":"OK"} -> succesful login / {"respone":"NO"} -> invalid email or password
# elif requestType == CHANGE_PASSWORD:
#     message[EMAIL] = Socket.email
#     #{"response":"OK"} -> acknoweldge
# elif requestType == DEPOSIT:
#     message[EMAIL] = Socket.email
#     #{"cash":"3500"}
# elif requestType == ADD_CART:
#     message[EMAIL] = Socket.email
#     #{"response":"OK"} -> successfuly added to cart / {"response":"NO","stock":"3"} -> not enough in stock
# elif requestType == REMOVE_CART:
#     message[EMAIL] = Socket.email
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
