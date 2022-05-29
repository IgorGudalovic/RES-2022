import socket,pickle,time,random
import constants.codes as codes

class Item:
    def __init__(self,code,value):
        self.code = code
        self.age = value

class WorkerState:
    # Pali i gasi Workere
    def _init_(self,dict):
        self.dict = dict

class Writer:
    #Create Connection
    def CreateConnectionLB(self):
        # Create a socket connection.
        try:
            clientLB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except:
            print('Socket making error!')

        try:
            clientLB.connect((socket.gethostname(), 8081))
        except:
            print('Socket connection error!')
        clientLB.close()
        return clientLB

    def CreateConnectionWorker(self):
        # Create a socket connection.
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except:
            print('Socket making error!')

        try:
            client.connect((socket.gethostname(), 8082))
        except:
            print('Socket connection error!')
        client.close()
        return client

    def SendWorkerState(self):
        client = self.CreateConnectionWorker()
        workerDict = {
            1:"ON",
            2:"ON",
            3:"ON",
            4:"ON"
        }
        variable = WorkerState(workerDict)
        state_data = pickle.dumps(variable)
        try:
            client.send(state_data)
            print('Item Sent to Server')                         
        except:
            print('Send error!')  
        pass


    # Salje podatke Load Balanceru svake 2 sekunde
    def RunDataSending(self):
        clientLB = self.CreateConnectionLB()

        listCodes= codes.Code.getList()
        while True:                    
            # Create an instance of Person to send to server.
            variable = Item(random.choice(listCodes),random.randint(1,500))
            # Pickle the object and send it to the server
            data_string = pickle.dumps(variable)
            
            try:
                clientLB.send(data_string)
                print('Item Sent to Server')                         
            except:
                print('Send error!')        
            time.sleep(2)               
            pass    