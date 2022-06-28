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

#For read and write image data
def convertToBinaryData(filename):
    # Convert digital data to binary format
    file = open(filename, 'rb')
    binaryData = file.read()
    return binaryData

def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    file = open(filename, 'wb')
    file.write(data)

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

def signup(dataobj, conn, addr):
    email = dataobj['email']
    password = dataobj['password']
    fName = dataobj['fname']
    lName = dataobj['lname']
    bDate = dataobj['bdate'] #'2022-01-18'
    country = dataobj['country']
    country = country[0].upper() + country[1:].lower()
    city = dataobj['city'].lower()
    job = dataobj['job']
    password = hashlib.md5(password.encode('UTF-8')).hexdigest()

    #validation
    #email is unique  USER(EMAIL, FNAME, LNAME, PASSWORD, BDATE, COUNTRY, CITY, JOB, CASH)
    mycursor.execute(f"""SELECT EMAIL FROM USER
                        WHERE EMAIL = '{email.lower()}'
    """)
    if (mycursor.rowcount > 0): #Account already exist
        result = mycursor.fetchone()
        dicto = {"response": "NO"} #Account already exist
        json_obj = json.dumps(dicto)  # JSON
        send(json_obj, conn, addr)
    else:  #Doesnt exist
        mycursor.execute(f"""SELECT city FROM LOC
                                     WHERE city = '{city}'
        """)
        if mycursor.rowcount == 0:
            loc_lock.acquire()
            mycursor.execute(f"INSERT INTO LOC values('{city}', {country}')")
            mydb.commit()
            loc_lock.release()
        user_lock.acquire()
        mycursor.execute(f"INSERT INTO USER values('{email.lower()}', '{fName}', '{lName}', '{password}', '{bDate}', '{city}', '{job}', '0')")
        mydb.commit()
        user_lock.release()

        dicto = {"response": "OK"} #Account registered
        json_obj = json.dumps(dicto)  # JSON
        send(json_obj, conn, addr)
        mydb.commit()
    #store hashed

def getItems(dataobj, conn, addr):
    email = dataobj['email']
    mycursor.execute("""SELECT * FROM ITEM
    """)
    list_of_tubles = mycursor.fetchall()
    """[
    item0 ("AHMED", "AYMAN",), dicto['items'][i][0]
    (),
    ()
    ]
    """
    dicto = {'items': list_of_tubles, 'msg': 'img'}
    json_obj = pickle.dumps(dicto)
    send_pickle(json_obj, conn, addr)

def getBalance(dataobj, conn, addr):
    email = dataobj['email']
    mycursor.execute(f"""SELECT CASH FROM USER
                        WHERE EMAIL = '{email.lower()}'
    """)
    data_obj = mycursor.fetchone()[0] #(3500, )
    dicto = {'balance': str(data_obj)}
    json_obj = json.dumps(dicto)
    send(json_obj, conn, addr)

def deposit(data_obj, conn, addr):
    email = data_obj['email']
    amount = int(data_obj['amount'])
    user_lock.acquire()
    mycursor.execute(f"""UPDATE USER
                        SET CASH = CASH + '{amount}'
                        WHERE EMAIL = '{email.lower()}'
    """)
    mydb.commit()
    user_lock.release()
    #send cash
    getBalance(data_obj, conn, addr)

    def getProfile(data_obj, conn, addr):
    email = data_obj['email']
    mycursor.execute(f"""SELECT EMAIL, FNAME, LNAME, BDATE, USER.CITY, LOC.COUNTRY, JOB, CASH
                        FROM USER, LOC
                        WHERE USER.CITY = LOC.CITY and EMAIL = '{email.lower()}'
    """)
    data_obj = mycursor.fetchone()
    # date = datetime.date(5)
    # date_now = datetime.date(data_obj[3])
    bdate = str(data_obj[3])
    dicto = {'email': data_obj[0], 'fname': data_obj[1], 'lname': data_obj[2], 'bdate': bdate, 'city': data_obj[4], 'country': data_obj[5], 'job': data_obj[6], 'cash': data_obj[7] }
    json_obj = json.dumps(dicto)
    send(json_obj, conn, addr)

def editProfile(dataobj, conn, addr):
    email = dataobj['email']
    fName = dataobj['fname']
    lName = dataobj['lname']
    bDate = dataobj['bdate']  # '2022-01-18'
    country = dataobj['country']
    city = dataobj['city']
    job = dataobj['job']
    #insert loc
    mycursor.execute(f"""SELECT city FROM LOC
                         WHERE city = '{city}'
            """)
    if mycursor.rowcount == 0:
        loc_lock.acquire()
        mycursor.execute(f"INSERT INTO LOC values('{city}', '{country}')")
        mydb.commit()
        loc_lock.release()
    #update user
    user_lock.acquire()
    mycursor.execute(f"""UPDATE USER
                        SET FNAME = '{fName}', LNAME = '{lName}', BDATE = '{bDate}', CITY = '{city}', JOB = '{job}'
                        WHERE EMAIL = '{email.lower()}'
    """)
    mydb.commit()
    user_lock.release()
    dicto = {'response': "OK"}
    json_obj = json.dumps(dicto)
    send(json_obj, conn, addr)

def passChange(data_obj, conn, addr):
    email = data_obj['email']
    old_pass = data_obj['password']
    new_pass = data_obj['new_password']
    hashed = hashlib.md5(old_pass.encode('UTF-8')).hexdigest()
    hashed_new = hashlib.md5(new_pass.encode('UTF-8')).hexdigest()
    mycursor.execute(f"""SELECT PASSWORD FROM USER
                         WHERE EMAIL = '{email.lower()}'
    """)
    #check old = saved_pass
    data_obj = mycursor.fetchone()
    if (hashed == data_obj[0]): #password is correct so update
        user_lock.acquire()
        mycursor.execute(f"""UPDATE USER
                             SET PASSWORD = '{hashed_new}'
                             WHERE EMAIL = '{email.lower()}'
""")
        mydb.commit()
        user_lock.release()
        dicto = {'response': 'OK'}
        json_obj = json.dumps(dicto)
        send(json_obj, conn, addr)
    else: #password is incorrect
        dicto = {'response': 'NO'}
        json_obj = json.dumps(dicto)
        send(json_obj, conn, addr)

def addToCart(data_obj, conn, addr):
    email = data_obj['email']
    name = data_obj['name'] # name - description
    desc = data_obj['description']

    # join item -> item_identifier to get itemID and insert into purchase
    mycursor.execute(f"""SELECT ITEMID
                        FROM ITEM, ITEM_IDENTIFIER
                        WHERE ITEM.NAME = ITEM_IDENTIFIER.NAME and ITEM.DESCRIPTION = ITEM_IDENTIFIER.DESCRIPTION and ITEM.NAME = '{name}' and ITEM.DESCRIPTION = '{desc}'
    """)
    itemId = mycursor.fetchone()[0] # [(), (), (),]

    mycursor.execute(f"""SELECT PURCHID FROM PURCHASES
                         WHERE EMAIL = '{email.lower()}' and ITEMID = '{itemId}' and STATUS = 0
""")
    # purchases_id = mycursor.fetchone()[0]
    if mycursor.rowcount == 0: #insert
        purchases_lock.acquire()
        mycursor.execute(f"""INSERT INTO PURCHASES(EMAIL, ITEMID, STATUS) values('{email.lower()}', '{itemId}', 0)
""")
        mydb.commit()
        purchases_lock.release()
        dicto = {'response': "OK"}  #added to cart
        json_obj = json.dumps(dicto)
        send(json_obj, conn, addr)
    else: #item already in cart
        dicto = {'response': "NO"} #item already in cart
        json_obj = json.dumps(dicto)
        send(json_obj, conn, addr)

#     else: #update + decrease_amount_of_items
#         purchases_lock.acquire()
#         mycursor.execute(f"""UPDATE PURCHASES
#                              SET QUANTITY = QUANTITY + '{quantity}'
#                              WHERE PURCHID = '{purchases_id}'
# """)
#         purchases_lock.release()

def deleteFromCart(data_obj, conn, addr):
    email = data_obj['email']
    name = data_obj['name']
    desc = data_obj['description']

    # join item -> item_identifier to get itemID and insert into purchase
    mycursor.execute(f"""SELECT ITEMID
                            FROM ITEM, ITEM_IDENTIFIER
                            WHERE ITEM.NAME = ITEM_IDENTIFIER.NAME and ITEM.DESCRIPTION = ITEM_IDENTIFIER.DESCRIPTION and ITEM.NAME = '{name}' and ITEM.DESCRIPTION = '{desc}'
        """)
    itemId = mycursor.fetchone()[0]  # [(), (), (),]
    purchases_lock.acquire()
    mycursor.execute(f"""DELETE FROM PURCHASES
                         WHERE EMAIL = '{email.lower()}' and ITEMID = '{itemId}' and STATUS = 0
    """)
    mydb.commit()
    purchases_lock.release()
    dicto = {'response': "OK"}
    json_obj = json.dumps(dicto)
    send(json_obj, conn, addr)

def getCart(data_obj, conn, addr):
    email = data_obj['email']
    mycursor.execute(f"""SELECT ITEM.NAME, ITEM.DESCRIPTION, ITEM.IMAGE, ITEM.PROCESSOR, ITEM.MEMORY, ITEM.STORAGE, ITEM.MANUFACT, ITEM.PRICE, ITEM.STOCK
                         FROM USER, PURCHASES, ITEM, ITEM_IDENTIFIER
                         WHERE STATUS = 0 and USER.EMAIL =  PURCHASES.EMAIL and USER.EMAIL = '{email}' and PURCHASES.ITEMID = ITEM_IDENTIFIER.ITEMID and ITEM_IDENTIFIER.NAME = ITEM.NAME and ITEM_IDENTIFIER.DESCRIPTION = ITEM.DESCRIPTION
""")
    items = mycursor.fetchall() #
    cart = 'cart'
    dicto = {'items': items, 'msg': cart}
    json_obj = pickle.dumps(dicto)
    send_pickle(json_obj, conn, addr)

def purchase(data_obj, conn, addr): #item by item they validate that its valid amount of money and they valid stock number
    email = data_obj['email']
    name = data_obj['name']
    desc = data_obj['description']
    quantity = data_obj['quantity']
    date_now = datetime.datetime.now()

    #USER
    mycursor.execute(f"""SELECT PRICE FROM ITEM
                         WHERE NAME = '{name}' and DESCRIPTION = '{desc}'
""")
    item_price = mycursor.fetchone()[0]
    total_price = quantity * item_price
    user_lock.acquire()
    mycursor.execute(f"""UPDATE USER
                         SET CASH = CASH - {total_price}
                         WHERE EMAIL = '{email}'
""")
    mydb.commit()
    user_lock.release()

    #ITEM
    item_lock.acquire()
    mycursor.execute(f"""UPDATE ITEM 
                         SET STOCK = STOCK - {quantity}
                         WHERE NAME = '{name}' and DESCRIPTION = '{desc}'
""")
    mydb.commit()
    item_lock.release()
    #ITEMID
    mycursor.execute(f"""SELECT ITEMID
                                FROM ITEM, ITEM_IDENTIFIER
                                WHERE ITEM.NAME = ITEM_IDENTIFIER.NAME and ITEM.DESCRIPTION = ITEM_IDENTIFIER.DESCRIPTION and ITEM.NAME = '{name}' and ITEM.DESCRIPTION = '{desc}'
            """)
    itemId = mycursor.fetchone()[0]  # [(), (), (),]

    #PRUCHASE history remove from cart and put in history
    purchases_lock.acquire()
    mycursor.execute(f"""UPDATE PURCHASES
                         SET STATUS = 1, QUANTITY = '{quantity}', TOTALPRICE = '{total_price}', DTIME = '{date_now}'
                         WHERE EMAIL= '{email}' and ITEMID = '{itemId}' and STATUS = 0
""")
    mydb.commit()
    purchases_lock.release()
    dicto = {'response': 'OK'}
    json_obj = json.dumps(dicto)
    send(json_obj, conn, addr)

def history(data_obj, conn, addr):
    email = data_obj['email']
    mycursor.execute(f"""SELECT ITEM_IDENTIFIER.NAME, ITEM_IDENTIFIER.DESCRIPTION, PURCHASES.QUANTITY, PURCHASES.DTIME, PURCHASES.TOTALPRICE
                         FROM USER, ITEM_IDENTIFIER, PURCHASES
                         WHERE USER.EMAIL = PURCHASES.EMAIL and USER.EMAIL = '{email}' and PURCHASES.ITEMID = ITEM_IDENTIFIER.ITEMID and status = 1
""")
    items = mycursor.fetchall()
    for i in range(len(items)):
        items[i] = list(items[i])
        items[i][3] = str(items[i][3])
        items[i] = tuple(items[i])
    # print(len(items))
    dicto = {'items': items}
    json_obj = json.dumps(dicto)
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


