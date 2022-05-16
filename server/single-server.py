import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()

server.bind((sys.argv[1], int(sys.argv[2]))) 
server.listen()
conn, address = server.accept()
conn.sendall(bytes("Welcome to this chatroom!".encode()))
while True:
    message = conn.recv(2048)
    print(message.decode())    
    
