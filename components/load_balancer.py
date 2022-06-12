import socket,pickle
import sys
sys.path.append('/home/x/Documents/GitHub/RES-2022/')
from models.item import Item
from components.worker import Worker
from multiprocessing import Process
from models.description import Description
from constants.codes import Code

brWorkera = 0
listaAktivnihWorkera = []
brojIstorijeWorkera = 0
desc = Description()
descList = []
descItemList = []
descID = 0
if __name__ == "__main__":  # ovo ispod se nece pozvati pri importovanju
    class LoadBalancer:
        server_socket = socket.socket()
        server_socket.bind(('127.0.0.1', 5001))
        server_socket2 = socket.socket()
        server_socket2.bind(('127.0.0.2', 5000))
        server_socket2.listen()
        server_socket.listen()

        def ReceiveItem():
            #Receives item
            items = []
            id = 0        
            conn, address = LoadBalancer.server_socket.accept()
            while True:
                id +=1
                dataRecv = conn.recv(4096)
                print("primio poruku")
                # receive data stream
                data = pickle.loads(dataRecv)   
                if not data:
                    # if data is not received break
                    break
                item = Item(data.code, data.value)
                items.append(item)
                pom = id - 1
                print(f"Item br {pom} code:{items[pom].code}  lista vrednost: {items[pom].value}\n")

                global descList
                global desc
                desc = LoadBalancer.ForwardDataPrepare(item)
                descList.append(desc)

            conn.close()  # close the connection

            #Formira objekat klase description 
        def ForwardDataPrepare(item):
            #description = Description()
            global descItemList
            global descID
            descID += 1
            #dataset
            if item.code == Code.CODE_ANALOG or item.code == Code.CODE_DIGITAL:
                dataset = 1
            if item.code == Code.CODE_CUSTOM or item.code == Code.CODE_LIMITSET:
                dataset = 2
            if item.code == Code.CODE_SINGLENOE or item.code == Code.CODE_MULTIPLENODE:
                dataset = 3
            if item.code == Code.CODE_CONSUMER or item.code == Code.CODE_SOURCE:
                dataset = 4

            #items 
            descItemList.append(item)
            description = Description(descID, descItemList, dataset)
            return description


        def ReceiveState():
            global brWorkera
            global desc
            global brojIstorijeWorkera
            #Receives state    
            LoadBalancer.server_socket2.listen()
            conn, address = LoadBalancer.server_socket2.accept()
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
                    brojIstorijeWorkera +=1
                    worker = Worker(brWorkera, True, True)
                    tWorker = Process(target=Worker.SaveData(worker,desc))
                    listaAktivnihWorkera.append(tWorker)
                else:
                    if  dataRecv == "OFF":
                        if brWorkera > 1:
                            listaAktivnihWorkera.remove(listaAktivnihWorkera[brWorkera-1])
                            brWorkera-=1
                            print(" WORKER UGASEN\n")
                        else:
                            print("GRESKA Nema vise workera\n")
                    else:
                        print("")
            conn.close()  # close the connection

        #def DoLoadBalancer():
    pReceiveItem = Process(target=LoadBalancer.ReceiveItem)
    pReceiveState = Process(target=LoadBalancer.ReceiveState)

    pReceiveItem.start()
    pReceiveState.start()
    br = 0
    for x in listaAktivnihWorkera:
        br+=1
        print(f"Uapljen worker: {br}")
        x.start()
