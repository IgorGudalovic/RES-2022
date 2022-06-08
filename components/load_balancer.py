import socket,pickle,threading
import sys
sys.path.append('/home/x/Documents/GitHub/RES-2022/')
from models.item import Item
import worker
from multiprocessing import Process

server_socket = socket.socket()
server_socket.bind(('127.0.0.1', 5005))
server_socket2 = socket.socket()
server_socket2.bind(('127.0.0.2', 5000))
server_socket2.listen()
server_socket.listen()

brWorkera = 0
listaWorkera = []
class LoadBalancer:

    def ReceiveItem():
        #Receives item
        items = []
        id = 0        
        conn, address = server_socket.accept()
        #print("Connection from: " + str(address))
        while True:
            #server_socket.listen()
            id +=1
            dataRecv = conn.recv(4096)
            # receive data stream
            data = pickle.loads(dataRecv)   
            if not data:
                # if data is not received break
                break
            item = Item(data.code, data.value)
            items.append(item)
            pom = id - 1
            print(f"Item br {pom} code:{items[pom].code}  lista vrednost: {items[pom].value}\n")
        conn.close()  # close the connection


    def ReceiveState():
        global brWorkera
        #Receives state    
        server_socket2.listen()
        conn, address = server_socket2.accept()
        while True:
            dataRecv = conn.recv(4096).decode("utf-8")
            print("\nstiglo:")
            print(dataRecv)
            # receive data stream
            if not dataRecv:
                # if data is not received break
                break
            print(f"Broj workera: {brWorkera}")
            if  dataRecv == "ON":
                print("NOVI WORKER UPALJEN\n")
                brWorkera +=1 
                tWorker = Process(target=worker.SaveData)
                listaWorkera.append(tWorker)
            else:
                if  dataRecv == "OFF":
                    if brWorkera > 1:
                        listaWorkera.remove(listaWorkera[brWorkera-1])
                        brWorkera-=1
                        print(" WORKER UGASEN\n")
                    else:
                        print("GRESKA Nema vise workera\n")
                else:
                    print("")
        conn.close()  # close the connection
        


pReceiveItem = Process(target=LoadBalancer.ReceiveItem)
pReceiveState = Process(target=LoadBalancer.ReceiveState)

pReceiveItem.start()
pReceiveState.start()

for x in listaWorkera:
    x.start()
