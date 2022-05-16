import socket
import select
import sys
from threading import Thread
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


if len(sys.argv) != 3:
    print("Try again Correct usage: IP address, port number")
    input = input().split
    while(len(input)!= 2):
        print("try again")
        message = sys.stdin.readline().split

IP_address = (sys.argv[1])
server.bind((IP_address, int(sys.argv[2])))
list_of_clients = []


def clientthread(conn, addr):
    conn.sendall(bytes("Welcome to this chatroom!",encoding='utf8'))

    start = time.time()
    while (time.time()-start<10):
        try:
            addr.send(bytes("still here", 'utf8'))
            message = conn.recv(2048)
            if message:

                print("<" + addr[0] + "> " + message)
               # Calls broadcast function to send message to all
                message_to_send = bytes("<" + addr[0] + "> " + message,'utf8')
                broadcast(message_to_send, conn)

            else:
                remove(conn)

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

start = time.time()
while (time.time()-start<10):
    
    server.listen()
    conn, addr = server.accept()
    list_of_clients.append(conn)
    # prints the address of the user that just connected 
    print(addr[0] + " connected")

    # creates and individual thread for every user
    thread = Thread(target = clientthread, args = (conn,addr ))
    thread.start()
    thread.join()

conn.close()
server.close()
