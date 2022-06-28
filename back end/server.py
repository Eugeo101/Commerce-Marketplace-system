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


def send(json_obj, conn, addr):
    msg_to_send = json_obj.encode(FORMAT)
    msg_length = len(msg_to_send)
    send_length = str(len(msg_to_send)).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(msg_to_send)
    # server.send() ? bcz con is between the client that send

def send_pickle(pickle_obj, conn, addr):
    msg_length = len(pickle_obj)
    send_length = str(len(pickle_obj)).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(pickle_obj)

def login(dataobj, conn, addr):
    email = dataobj['email']
    password = dataobj['password'] #string
    hashed = hashlib.md5(password.encode('UTF-8')).hexdigest() #128 bit => 32 char
    #get from database
    mycursor.execute(f"""SELECT PASSWORD FROM USER
                        WHERE EMAIL = '{email.lower()}'
    """)
    if (mycursor.rowcount > 0): #email exsist check password
        if hashed == str(mycursor.fetchone()[0]): #if password exist send object
            dicto = {"response": 'OK'}
            json_obj = json.dumps(dicto) #JSON
            send(json_obj, conn, addr)
        else: #password doesnt exist
            dicto = {"response": "Password is incorrect"}
            json_obj = json.dumps(dicto)  # JSON
            send(json_obj, conn, addr)
    else: #email doesnt exsist
        dicto = {"response": "This Account Doesnt exist"}
        json_obj = json.dumps(dicto) #
        send(json_obj, conn, addr)






def start(): #start server and get connection then handle this connection through function like handle_client
    server.listen() #listen for request
    print(f"[LISTENING] server is listening on {SERVER}:{PORT}")
    while True: #server is on always untill server crashs
        conn, addr = server.accept() #wait for new connection to server and blocks all lines after it till connection happen
        #conn , address means: (connection between client & server AND address (which pc wanted this: its (ip, port)))
        thread = threading.Thread(target=handle_client, args=(conn, addr)) #each new connection is thread run some function on server
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}\n") #amount of threads(users) on sever

def handle_client(conn, addr):
    print(f"[CLIENT CONNECTED] {addr} connected.\n")
    connnected = True
    while(connnected):
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)  # blocking line wait till client give msg!! args is no of bytes we recive (by header)
            # decode from coded(byte) to data (utf-8) string
            # recive 64 bytes contain number of bytes then decode
        except:
            print(f"[CONNECTION FAILED] connection with {addr} unexpectedly failed..\n")
            connnected = False
            break
        if msg_length:
            msg_length = int(msg_length) #convert string (result of decode into number)
            msg = conn.recv(msg_length).decode(FORMAT) #recive len of bytes and decode each one
            if msg == DISCONNECT_MESSAGE: #if msg is !Disconect just leave connection with server
                print(f"[CLIENT DISCONNECT] client of Address {addr} disconnected..\n")
                connnected = False
                break
            # return_obj = pickle.loads(msg)
            data_obj = json.loads(msg)  # load and return dictionary

            ##LOGIC
            print(f"[{addr}] {data_obj}\n")  # here we printed msg only (logic)
            if data_obj['request'] == LOGIN:
                login(data_obj, conn, addr)
            elif data_obj['request'] == CREATE_ACCOUNT:
                signup(data_obj, conn, addr)
            elif data_obj['request'] == GET_ITEMS:
                getItems(data_obj, conn, addr)
            elif data_obj['request'] == GET_BALANCE:
                getBalance(data_obj, conn, addr)
            elif data_obj['request'] == DEPOSIT:
                deposit(data_obj, conn, addr)
            elif data_obj['request'] == GET_PROFILE:
                getProfile(data_obj, conn, addr)
            elif data_obj['request'] == EDIT_PROFILE:
                editProfile(data_obj, conn, addr)
            elif data_obj['request'] == CHANGE_PASSWORD:
                passChange(data_obj, conn, addr)
            elif data_obj['request'] == SEARCH:
                searchItems(data_obj, conn, addr)
            elif data_obj['request'] == ADD_ITEM:
                addToCart(data_obj, conn, addr)
            elif data_obj['request'] == REMOVE_ITEM:
                deleteFromCart(data_obj, conn, addr)
            elif data_obj['request'] == GET_CART:
                getCart(data_obj, conn, addr)
            elif data_obj['request'] == PURCHASE:
                purchase(data_obj, conn, addr)
            elif data_obj['request'] == HISTORY:
                history(data_obj, conn, addr)
            elif data_obj['request'] == 'Add_Item':
                addItem(data_obj, conn, addr)



    conn.close() #disconnect connection


