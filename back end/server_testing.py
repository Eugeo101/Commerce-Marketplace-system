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
    response_length = client.recv(HEADER).decode(FORMAT) #'4'
    if response_length:
        response_length = int(response_length) #4
        response_msg = client.recv(response_length)
        try:
            response_msg_json = response_msg.decode(FORMAT) #json
            response_msg_json = json.loads(response_msg_json) #json -> dicto
            print(f"[SERVER RESPONSE] {response_msg_json}")  # some number of bytes
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