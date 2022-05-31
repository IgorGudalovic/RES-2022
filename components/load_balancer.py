import socket,pickle, time, threading
import sys
sys.path.append('/home/x/Documents/GitHub/RES-2022/')
from threading import Thread
from models.item import Item
from models.description import Description
from constants.codes import Code
import worker

def WorkerStates(data):
    worker1 = threading.Thread(target=worker.SaveData())
    worker2 = threading.Thread(target=worker.SaveData())
    worker3 = threading.Thread(target=worker.SaveData())
    worker4 = threading.Thread(target=worker.SaveData())
    listaWorkera = []
    listaWorkera.append(worker1)
    listaWorkera.append(worker2)
    listaWorkera.append(worker3)
    listaWorkera.append(worker4)

    br=0
    for string in data:
        
        if  string == "ON":
            listaWorkera[br].start()
            listaWorkera[br].join()
        else:
            break
        br+=1
    print(f"Thread {listaWorkera[br]} je {string}")


def instancirajDesc(code:Code):
    if code== Code.CODE_ANALOG or code== Code.CODE_DIGITAL:
        desc = Description(id, items,1)
    elif code == Code.CODE_CUSTOM or code == Code.CODE_LIMITSET:
        desc = Description(id, items,2)
    elif code == Code.CODE_SINGLENOE or code == Code.CODE_MULTIPLENODE:
        desc = Description(id, items,3)
    else :
        desc = Description(id, items,4)    
    return desc

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

WorkerStates(data1)

items = []
#prima item
id = 0
while True:
    id +=1
    dataRecv = conn.recv(4096)
    # receive data stream. it won't accept data packet greater than 1024 bytes
    data = pickle.loads(dataRecv)   
    if not data:
        # if data is not received break
        break
    item = Item(data.code, data.value)
    items.append(item)
    desc = instancirajDesc(data.code)
    for x in items:
        print(f"Lista code:{x.code}  lista vrednost: {x.value}\n")
    print(f"from connected user: {data.code} {data.value}\n")
conn.close()  # close the connection
