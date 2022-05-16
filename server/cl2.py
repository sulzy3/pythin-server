import socket
import sys
from threading import Thread
import os
from win32com.client import GetObject

WMI = GetObject('winmgmts:')
processes = WMI.InstancesOf('Win32_Process')
p = WMI.ExecQuery('select * from Win32_Process where Name="cmd.exe"')[2]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
    print("Correct usage: script, IP address, port number")
    exit()


def write():
    while True:
        message = sys.stdin.readline()
        server.sendall(message.encode())
        if message == 'bye\n':
            # kill cmd
            os.system("taskkill /pid " + str(p.Properties_('ProcessId').Value))
            break


def listen():
    while True:
        message = server.recv(2048)
        print(message.decode())


IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.connect((IP_address, Port))
t1 = Thread(target=write)
t2 = Thread(target=listen)

t1.start()
t2.start()
