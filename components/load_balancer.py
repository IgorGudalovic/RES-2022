import socket,pickle
import sys
sys.path.append('/home/x/Documents/GitHub/RES-2022/')
from models.item import Item
from components.worker import Worker
from multiprocessing import Process
from models.description import Description
from constants.codes import Code

brWorkera = 1
listaAktivnihWorkera = []
brojIstorijeWorkera = 1
desc = Description()
descList = []
descItemList = []
descID = 0

class LoadBalancer:       
    def CreateServerSocket1():
        try:            
            server_socket = socket.socket()
            server_socket.bind(('127.0.0.1', 5001))
            server_socket.listen()
            conn, address = server_socket.accept()
            return conn
        except:
            exit()
    def CreateServerSocket2():
        try:            
            server_socket = socket.socket()
            server_socket.bind(('127.0.0.2', 5000))
            server_socket.listen()
            conn, address = server_socket.accept()
            return conn
        except:
            exit()

    def ReceiveItem():
        items = []
        id = 0        
        conn = LoadBalancer.CreateServerSocket1()
        while True:
            id +=1
            dataRecv = conn.recv(4096)
            print("primio Item")
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

    #bafer radi na principu FIFO
    def Buffer():
        global descList
        try:
            desc = descList.pop(0)
            return desc
        except:
            print("Descritpion lista je prazna")

    def ReceiveState():
        global brWorkera
        global descList
        global brojIstorijeWorkera
        conn = LoadBalancer.CreateServerSocket2()
        while True:
            dataRecv = conn.recv(4096).decode("utf-8")
            print("\nStiglo:")
            print(dataRecv)
            if not dataRecv:
                # if data is not received break
                break
            print(f"Broj workera: {brWorkera}")
            if  dataRecv == "ON":
                print("NOVI WORKER UPALJEN\n")                
                worker = Worker(brWorkera, True, True)
                desc = LoadBalancer.Buffer()
                tWorker = Process(target=Worker.SaveData, args=(worker,desc))
                listaAktivnihWorkera.append(tWorker)
                brojIstorijeWorkera +=1
                brWorkera +=1 

                br = 0
                while br<len(listaAktivnihWorkera):                    
                    print(f"Upaljen worker: {br}")
                    listaAktivnihWorkera[br].start() 
                    br+=1

            elif  dataRecv == "OFF":
                if brWorkera > 1:
                    listaAktivnihWorkera.remove(listaAktivnihWorkera[brWorkera-1])
                    brWorkera-=1
                    print(" WORKER UGASEN\n")
                else:
                    print("GRESKA Nema vise workera\n")

        conn.close()
           
        
if __name__ == "__main__":  # ovo ispod se nece pozvati pri importovanju
    pReceiveItem = Process(target=LoadBalancer.ReceiveItem)
    pReceiveState = Process(target=LoadBalancer.ReceiveState)

    pReceiveItem.start()
    pReceiveState.start()
    
