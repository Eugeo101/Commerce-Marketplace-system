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