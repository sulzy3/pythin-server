import socket
import select
import sys
import threading
from _thread import start_new_thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()
    IP_address = str(sys.argv[1])
    server.bind((IP_address, int(sys.argv[2])))

list_of_clients = []


def client_thread(connection, address):
    connection.send("Welcome to this chatroom!")

    while True:
        try:
            message = connection.recv(2048)
            if message:

                print("<" + address[0] + "> " + message)

                # Calls broadcast function to send message to all
                message_to_send = "<" + addr[0] + "> " + message
                broadcast(message_to_send, connection)

            else:
                remove(connection)

        except:
            continue


def broadcast(message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(message)
            except:
                clients.close()

                # if the link is broken, we remove the client 
                remove(clients)


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


while True:
    server.listen()
    conn, address = server.accept()
    list_of_clients.append(conn)
    # prints the address of the user that just connected 
    print(address[0] + " connected")

    # creates and individual thread for every user  
    # that connects 
    start_new_thread(client_thread, (conn, address))

conn.close()
server.close()
