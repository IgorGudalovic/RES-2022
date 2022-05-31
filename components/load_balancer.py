import socket,pickle
import sys
sys.path.append('/home/x/Documents/GitHub/RES-2022/')
from threading import Thread
from models.item import Item

list = []
def dodajUListuItema(item:Item):
    return list.append(item)

#prima worker state
server_socket = socket.socket()
server_socket.bind((socket.gethostname(), 5001))
server_socket.listen()
conn, address = server_socket.accept()
print("Connection from: " + str(address))
dataRecv = conn.recv(4096)
data1 = []
data1 = pickle.loads(dataRecv)
print(f"from connected user: {data1}")
#prima item
while True:
    dataRecv = conn.recv(4096)
    # receive data stream. it won't accept data packet greater than 1024 bytes
    data = pickle.loads(dataRecv)   
    if not data:
        # if data is not received break
        break
    item = Item(data.code, data.value)
    dodajUListuItema(item)
    for x in list:
        print(f"Lista code:{x.code}  lista vrednost: {x.value}\n")
    print(f"from connected user: {data.code} {data.value}\n")
conn.close()  # close the connection
