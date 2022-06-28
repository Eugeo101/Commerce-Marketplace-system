from user import User
from item import Item
from purchases import Purchases
# import time
import socket
import threading
import pickle
import json
import hashlib
import datetime


#server configurations
PORT = 5050
# SERVER = "25.7.104.250" # 25.7.104.250
# "2620:9b::1907:68fa"
SERVER = socket.gethostbyname(socket.gethostname()) #get my pc IPv4 address => 25.7.104.250
# print(SERVER)
# print(socket.gethostname()) get my pc name
ADDR = (SERVER, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #our socket
server.bind(ADDR) #socket binded to ip and port no.

HEADER = 64 # header of first msg to server [64BYTE msg]
FORMAT = 'UTF-8' # to decode msg into UTF-8 decoded length is less that orignal length msg
DISCONNECT_MESSAGE = "!DISCONNECT"


#database configurations
import mysql.connector #pip install mysql-connector-python
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ahmedate123",
    database="NMatketdb"
)
mycursor = mydb.cursor(buffered=True, dictionary=False) # cursor manpulate mysql

#synchronization method
user_lock = threading.Lock() #user
loc_lock = threading.Lock() #loc
item_lock = threading.Lock()#item
purchases_lock = threading.Lock()  #purch


CREATE_ACCOUNT = "CREATE_ACCOUNT"
LOGIN = "LOGIN"
EDIT_PROFILE = "EDIT_PROFILE"
CHANGE_PASSWORD = "CHANGE_PASSWORD"
DEPOSIT = "DEPOSIT"
GET_BALANCE = "GET_BALANCE"
GET_ITEMS = "GET_ITEMS"
GET_PROFILE = "GET_PROFILE"
SEARCH = "SEARCH_ITEMS"
ADD_ITEM = "ADD_ITEM"
REMOVE_ITEM = "REMOVE_ITEM"
GET_CART = "GET_CART"
PURCHASE = "PURCHASE"
HISTORY = "HISTORY"

def start(): #start server and get connection then handle this connection through function like handle_client
    server.listen() #listen for request
    print(f"[LISTENING] server is listening on {SERVER}:{PORT}")
    while True: #server is on always untill server crashs
        conn, addr = server.accept() #wait for new connection to server and blocks all lines after it till connection happen
        #conn , address means: (connection between client & server AND address (which pc wanted this: its (ip, port)))
        thread = threading.Thread(target=handle_client, args=(conn, addr)) #each new connection is thread run some function on server
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}\n") #amount of threads(users) on sever