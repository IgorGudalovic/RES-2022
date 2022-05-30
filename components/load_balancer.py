import socket,pickle 
import sys
sys.path.append('/home/x/Documents/GitHub/RES-2022/')
import models.item as item
import models.description as description
import constants.codes as codes
from threading import Thread
import components.writer as writer


class LoadBalancer:
    def __init__(self, port):
        self.port = port
        pass
    buffer = []
    id = 0

    #Formiranje uticice i postavljanej u stanje listening
    def InitalizeServer(self):
        try:
            LBSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            print("socket creation failed with error %s" %(err))

        try:    
            LBSocket.bind((socket.gethostname(), self.port))
        except:
            print("socket binding failed with error %s" %(err))
            LBSocket.close()

        LBSocket.listen()
        print("Waiting for connections...")
        return LBSocket

      
    # Prima podatke od Writer komponente
    def ReceiveData(self):
        data = pickle.loads(conn.recv())
        return data

    # Prosledjuje primljene podatke slobodnim Workerima
    # Salje podatke koristeci Description strukturu
    def ForwardData(self, data: description.Description):
        #kreiranje tredova

        data = pickle.dumps(data)
        try:
            #proslledi data tredovimma
            return True
        except:
            print('Forward message failed')
            return False

        
    #Formira objekat klase description 
    def ForwardDataPrepare(self,data):
        self.data = item.Item(data) 
        self.description = description.Description()

        #id
        id+=1
        self.description.id =id 

        #dataset
        if self.data.code == codes.Code.CODE_ANALOG or self.data.code == codes.Code.CODE_DIGITAL:
            self.description.dataset = 1
        elif self.data.code == codes.Code.CODE_CUSTOM or self.data.code == codes.Code.CODE_LIMITSET:
            self.description.dataset = 2
        elif self.data.code == codes.Code.CODE_SINGLENOE or self.data.code == codes.Code.CODE_MULTIPLENODE:
            self.description.dataset = 3
        elif self.data.code == codes.Code.CODE_CONSUMER or self.data.code == codes.Code.CODE_SOURCE:
            self.description.dataset = 4

        #items 
        self.description.items.append(self.data)
        
        return self.description

    def WorkerUpdate(self):
        data = pickle.loads(conn2.recv())

        data= writer.WorkerState(data)
        print('Igor sent message')
        #logika 
        pass
    

LBData = LoadBalancer(8081)
LBDataSocket = LBData.InitalizeServer()
LBWorker = LoadBalancer(8082)
LBWorkerSocket = LBWorker.InitalizeServer()
while True:
    conn2, addr2 =LBWorkerSocket.accept()
    LBWorker.WorkerUpdate()

    conn, addr = LBDataSocket.accept()
    print ('Got connection from', addr )
    while True:
        data = LoadBalancer.ReciveData()
        #upis u bazu ------------------------------------
        data = LoadBalancer.ForwardDataPrepare(data)
        
        if not LoadBalancer.ForwardData(data):
            break #ako ne uspe da psoalje


