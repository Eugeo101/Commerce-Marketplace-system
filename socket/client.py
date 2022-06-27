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

requestType = LOGIN

def customDecoder(Dict):
    return namedtuple('X', Dict.keys())(*Dict.values())

def send(msg):
    message = json.dumps(msg)
    print("Message Sent:" + msg)
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


def receive():
    msg_length = client.recv(HEADER).decode(FORMAT)
    msg_length = int(msg_length)
    msg = client.recv(msg_length).decode(FORMAT)
    print("Message Received:" + msg)
    return json.loads(msg, object_hook=customDecoder)


login = {"email":"Ahmed@gmail.com","password":"Ahmed50"}
change_password = {"email":"Ahmed@gmail.com","password":"Ahmed50","new_password":"Ahmed40"}
deposit = {"email":"Ahmed@gmail.com","amount":"500"}
cart = {"email":"Ahmed@gmail.com","item":"30"}
balance = "3000"
server_response = "OK"
get_request = {"email":"Ahmed@gmail.com"}
account_info = {"fname":"Ahmed","lname":"Alaa","email":"Ahmed@gmail.com","password":"Ahmed50","bdate":"2000\01\01","country":"Egypt","city":"Cairo","job":"Worker"}
edit_info = {"fname":"Ahmed","lname":"Alaa","email":"Ahmed@gmail.com","bdate":"2000\01\01","country":"Egypt","city":"Cairo","Job":"Worker"}
profile = {"fname":"Ahmed","lname":"Alaa","email":"Ahmed@gmail.com","bdate":"2000\01\01","country":"Egypt","city":"Cairo","Job":"Worker","cash":"3000"}
if requestType == CREATE_ACCOUNT:
    account_info["request"] = CREATE_ACCOUNT
    send(account_info)
    server_response = receive() #{"respone":"OK"} -> successful creation of account / {"respone":"NO"} -> account already exists
elif requestType == EDIT_PROFILE:
    edit_info["request"] = EDIT_PROFILE
    send(edit_info)
    server_response = receive() #{"respone":"OK"} -> successful creation of account / {"respone":"NO"} -> email already exists
elif requestType == GET_PROFILE:
    get_request["request"] = GET_PROFILE
    send(get_request)
    profile = receive() #{"fname":"Ahmed","lname":"Alaa","email":"Ahmed@gmail.com","bdate":"2000\01\01","country":"Egypt","city":"Cairo","job":"Worker","cash":"3000"}
elif requestType == LOGIN:
    login["request"] = LOGIN
    send(login)
    server_response = receive() #{"respone":"OK"} -> succesful login / {"respone":"NO"} -> invalid email or password
elif requestType == CHANGE_PASSWORD:
    change_password["request"] = CHANGE_PASSWORD
    send(change_password)
    server_response = receive() #{"response":"OK"} -> acknoweldge
elif requestType == DEPOSIT:
    deposit["request"] = DEPOSIT
    send(deposit) #{"balance":"3500"}
elif requestType == BUY:
    get_request["request"] = BUY
    send(get_request)
    server_response = receive() #{"response":"OK","balance":"3000"} -> successful buy / {"response":"NO","items":[]}  -> not enough in stock
elif requestType == ADD_CART:
    cart["request"] = ADD_CART
    send(cart)
    server_response = receive() #{"response":"OK"} -> successfuly added to cart / {"response":"NO","stock":"3"} -> not enough in stock
elif requestType == REMOVE_CART:
    cart["request"] = REMOVE_CART
    send(cart)
    server_response = receive() #{"response":"OK"} -> successful removal
elif requestType == GET_CART:
    get_request["request"] = GET_CART
    send(get_request)
    receive() 
elif requestType == GET_BALANCE:
    get_request = {"request":GET_BALANCE}
    send(get_request)
    cash = receive() #{"balance":"3500"}
elif requestType == GET_ITEMS:
    get_items = {"request":"GET_ITEMS"}
    send(get_items)
    items = receive() #{"items":[]}

# send("Hello World!")
# input()
# send("Hello Everyone!")
# input()
# send("Hello Tim!")
# input()
# send("Object")
# receive()
# input()
# send({1:"hi", 2: "there"})
# input()

# send(DISCONNECT_MESSAGE)