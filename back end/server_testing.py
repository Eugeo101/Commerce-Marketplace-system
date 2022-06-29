from user import User
from item import Item
from purchases import Purchases
import json
import pickle
import socket
import os


#Server configuration
PORT = 5050
SERVER = "25.7.104.250" #102.58.127.16 #'0.0.0.0', 5050
# SERVER = "25.7.104.250" #of running server
ADDR = (SERVER, PORT)
# scoket and its connection to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #our socket
client.connect(ADDR) #server is connected now lets send

HEADER = 64 #header of first msg to server
FORMAT = 'UTF-8' #to decode
DISCONNECT_MESSAGE = "!DISCONNECT"

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

def send(msg): #"Ahmed" => [bytes bytes bytes bytes] [HEADER msg]
    message = msg.encode(FORMAT) #byte format encoded msg #  '123' => bytes b'x/ab24' => ['4'.encode => 15bytes]
    msg_length = len(message) #bytes(encoded msg) format length 2
    send_length = str(msg_length).encode(FORMAT) #encoded length of bytes msg as string
    send_length += b' ' * (HEADER - len(send_length)) #for padding till 64 of header
    client.send(send_length) # to send header
    client.send(message) #massage


#client recive response from server
def receive():
    response_length = client.recv(HEADER).decode(FORMAT) #'4'
    if response_length:
        response_length = int(response_length) #4
        response_msg = client.recv(response_length)
        try:
            response_msg_json = response_msg.decode(FORMAT) #json
            response_msg_json = json.loads(response_msg_json) #json -> dicto
            print(f"[SERVER RESPONSE] {response_msg_json}")  # some number of bytes
            return response_msg_json
        except:
            response_msg = pickle.loads(response_msg)  # json -> dicto
            directory = "assests"
            parent_dir = os.getcwd()
            path = os.path.join(parent_dir, directory)
            if (os.path.exists(path) == False):
                # create folder
                os.mkdir(path)

            # mapping bytes -> name
            caption = 'Image'
            # print(response_msg)
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

#login
input()
email = "ahmed.com"
passwd = "password"
dicto = {'email': email, 'password': passwd}
dicto['request'] = LOGIN
json_obj = json.dumps(dicto) #dumps: convert to json
send(json_obj)
response_msg = receive()
print(response_msg)

input()
email = "ahmed.com"
passwd = "password1"
dicto = {'email': email, 'password': passwd}
dicto['request'] = LOGIN
json_obj = json.dumps(dicto)
send(json_obj)
response_msg = receive()
print(response_msg)

input()
email = "ergrehthrhncvhgfdhsehth.com"
passwd = "password1"
dicto = {'email': email, 'password': passwd}
dicto['request'] = LOGIN
json_obj = json.dumps(dicto)
send(json_obj)
response_msg = receive()
print(response_msg)

#signup
input()
ahmed = User("Ahmedayman58134@gmail.com")
ahmed.password = 'Ahmedate123'
ahmed.fname = "Ahmed"
ahmed.lname = "Ayman"
ahmed.bdate = "2000-01-07"
ahmed.country = "Egypt"
ahmed.city = "cairo"
ahmed.job = "Enginner"
dicto = ahmed.__dict__
dicto['request'] = CREATE_ACCOUNT
json_obj = json.dumps(ahmed.__dict__) #convert to dictionary to be converted to json
send(json_obj)
response_msg = receive()
print(response_msg)


# get items
input()
email = "ahmedayman58134@gmail.com" #
dicto = {'email': email}
dicto['request'] = GET_ITEMS
json_obj = json.dumps(dicto)
send(json_obj)
response_msg = receive()
print(response_msg)

#edit deposit
input()
email = "ahmedayman58134@gmail.com" #
dicto = {'email': email, 'amount': '500'}
dicto['request'] = DEPOSIT
json_obj = json.dumps(dicto)
send(json_obj)
response_msg = receive()
print(response_msg)

#editProfile
input()
dicto = {"fname":"Adham", "lname":"Mohamed", "email": 'ahmedayman58134@gmail.com',"bdate":"2000-07-01", "country":"Egypt", "city":"Alex", "job":"Worker"}
dicto['request'] = EDIT_PROFILE
json_obj = json.dumps(dicto)
send(json_obj)
response_msg = receive()
print(response_msg)

#getProfile
input()
email = "ahmedayman58134@gmail.com" #
dicto = {'email': email}
dicto['request'] = GET_PROFILE
json_obj = json.dumps(dicto)
send(json_obj)
response_msg = receive()
print(response_msg)

#password
input()
email = "ahmed.com" #
old_pass = "password" #
new_pass = "Ahmedate123" #
dicto = {'email': email, 'password': old_pass, 'new_password': new_pass}
dicto['request'] = CHANGE_PASSWORD
json_obj = json.dumps(dicto)
send(json_obj)
response_msg = receive()
print(response_msg)

#search
input()
dicto = {'name': 'mouse'}
dicto['request'] = SEARCH
json_obj = json.dumps(dicto)
send(json_obj)
response_msg = receive()
print(response_msg)

#add_item
input()
name ='laptop'
desc = 'this is the best laptop'
dicto = {'email': 'ahmedayman58134@gmail.com', 'name': name, 'description': desc}
dicto['request'] = ADD_ITEM
json_obj = json.dumps(dicto)
send(json_obj)
response_msg = receive()
print(response_msg)

#add item
input()
name = 'mouse'
description = 'this is the best mouse'
dicto = {'email': 'ahmedayman58134@gmail.com', 'name': name, 'description': description}
dicto['request'] = ADD_ITEM
json_obj = json.dumps(dicto)
send(json_obj)
response_msg = receive()
print(response_msg)


#GetCart
input()
dicto = {'email': 'ahmedayman58134@gmail.com'}
dicto['request'] = GET_CART
json_obj = json.dumps(dicto)
send(json_obj)
response_msg = receive()
print(response_msg)

#RemoveCart
input()
name ='laptop'
desc = 'this is the best laptop'
dicto = {'email': 'ahmedayman58134@gmail.com', 'name': name, 'description': desc}
dicto['request'] = REMOVE_ITEM
json_obj = json.dumps(dicto)
send(json_obj)
response_msg = receive()
print(response_msg)

#GetCart
input()
dicto = {'email': 'ahmedayman58134@gmail.com'}
dicto['request'] = GET_CART
json_obj = json.dumps(dicto)
send(json_obj)
response_msg = receive()
print(response_msg)

#                                                                               PURCHASE

#add item
input()
name = 'mouse'
description = 'this is the best mouse'
dicto = {'email': 'ahmedayman58134@gmail.com', 'name': name, 'description': description}
dicto['request'] = ADD_ITEM
json_obj = json.dumps(dicto)
send(json_obj)
response_msg = receive()
print(response_msg)

#purchase item
input()
name = 'mouse'
description = 'this is the best mouse'
quantity = 10
dicto = {'email': 'ahmedayman58134@gmail.com', 'name': name, 'description': description, 'quantity': quantity}
dicto['request'] = PURCHASE
json_obj = json.dumps(dicto)
send(json_obj)
response_msg = receive()
print(response_msg)

#GetCart
input()
dicto = {'email': 'ahmedayman58134@gmail.com'}
dicto['request'] = GET_CART
json_obj = json.dumps(dicto)
send(json_obj)
response_msg = receive()
print(response_msg)

#history
input()
dicto = {'email': 'ahmedayman58134@gmail.com'}
dicto['request'] = HISTORY
json_obj = json.dumps(dicto)
send(json_obj)
response_msg = receive()
print(response_msg)

#add item and it's identifier
input()
path = "C:\\3rd Electrical Computer AI\\2nd term\\Parallel and Distributed Systems\\project\\server\\assests\\Image1.jpeg"
dicto = {'image': path}
dicto['request'] = 'Add_Item'
json_obj = json.dumps(dicto)
send(json_obj)
response_msg = receive()
print(response_msg)

send(DISCONNECT_MESSAGE)