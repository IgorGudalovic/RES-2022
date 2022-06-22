import socket,pickle
import sys
sys.path.append('/home/x/Documents/GitHub/RES-2022/')
from models.item import Item
from components.worker import Worker
from multiprocessing import Process
from models.description import Description
from constants.codes import Code
import threading
from constants.data_sets import DataSet

brWorkera = 1
listaAktivnihWorkera = []
brojIstorijeWorkera = 1
desc = Description(1,[], DataSet.DataSet_1)
descList = []
descItemList = []
descID = 0

if __name__ == "__main__":  # ovo ispod se nece pozvati pri importovanju

    class LoadBalancer:
        def __init__(self, descList:list):
            self.descList = descList
        @staticmethod
        def CreateServerSocket1():
            try:            
                server_socket = socket.socket()
                server_socket.bind(('127.0.0.1', 5001))
                server_socket.listen()
                conn, address = server_socket.accept()
                return conn
            except:
                exit()
        @staticmethod
        def CreateServerSocket2():
            try:            
                server_socket = socket.socket()
                server_socket.bind(('127.0.0.2', 5000))
                server_socket.listen()
                conn, address = server_socket.accept()
                return conn
            except:
                exit()

        def ReceiveItem(self):
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

                #global desc
                #desc = LoadBalancer.ForwardDataPrepare(item)
                lb = LoadBalancer([])
                self.descList.append(lb.ForwardDataPrepare(item))

            conn.close()  # close the connection

            #Formira objekat klase description 
        def ForwardDataPrepare(self, item):
            #description = Description()
            global descItemList
            global descID
            descID += 1
            #dataset
            if item.code == Code.CODE_ANALOG or item.code == Code.CODE_DIGITAL:
                dataset = DataSet.DataSet_1
            if item.code == Code.CODE_CUSTOM or item.code == Code.CODE_LIMITSET:
                dataset = DataSet.DataSet_2
            if item.code == Code.CODE_SINGLENOE or item.code == Code.CODE_MULTIPLENODE:
                dataset = DataSet.DataSet_3
            if item.code == Code.CODE_CONSUMER or item.code == Code.CODE_SOURCE:
                dataset = DataSet.DataSet_4

            #items 
            descItemList.append(item)
            description = Description(descID, descItemList, dataset)
            return description

        #bafer radi na principu FIFO
        def Buffer(self):
            try:
                desc = self.descList.pop(0)
                return desc
            except:
                print("Descritpion lista je prazna")

        def ReceiveState(self):
            global brWorkera
            #global descList
            global brojIstorijeWorkera
            conn = self.CreateServerSocket2()
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
                    description = self.Buffer()
                    tWorker = Process(target=Worker.SaveData, args=(worker,description))
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
    
    dList = []
    lb = LoadBalancer(dList)
    pReceiveItem = threading.Thread(target=lb.ReceiveItem)
    pReceiveState = threading.Thread(target=lb.ReceiveState)

    pReceiveItem.start()
    pReceiveState.start()