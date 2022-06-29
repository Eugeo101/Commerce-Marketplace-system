# parralel-project

This is an application where an interaction between clients and a server as a centralized client-server architecture, where:

## A client (GUI): is a marketplace system where users can:
1- Create new account.

2- Login.

3- View the items in the system.

4- ADD / EDIT / Remove items from his cart.

5- Search for items.

6- View the account info.

7- Edit the account info.

8- Change the password.

9- Deposit cash.

10- Purchase items.

11- Show the purchase history.

12- View the cart.

## How a client connects to the server:
Each client sends a request message to the server (using sockets), the server accepts the client message and create a connection by creating a thread to handle each client, and the connection doesn't close until the client send a disconnection message to the server.

items and user info. and user purchases history and user cart are stored in database using SQL
