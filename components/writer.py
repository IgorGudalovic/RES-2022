import sys
import threading
sys.path.append('C:/Users/Ema/OneDrive/Dokumenti/GitHub/RES-2022')
import socket, pickle, time, random
import constants.codes as codes
from models.item import Item
from multiprocessing import Process
from components.logger import Logger


logMessage1 = "Data sent to the load balancer"
logMessage2 = "Active worker changed"

class Writer:

    @staticmethod
    def CreateClientSocket1():
        try:
            client_socket = socket.socket()
            client_socket.connect(('127.0.0.1', 5001))
            Logger.Log("Writer component conected to load balancer")
            return client_socket
        except:
            exit()
    @staticmethod
    def CreateClientSocket2():
        try:
            client_socket2 = socket.socket()
            client_socket2.connect(('127.0.0.2', 5000))
            Logger.Log("Writer component conected to load balancer")
            return client_socket2
        except:
            exit()


    def SendItem(self):
        client_socket = self.CreateClientSocket1()
        listCodes = []
        for code in codes.Code:
            listCodes.append(code.name)
        while True:    
            rand1 = random.choice(listCodes)
            rand2 = random.randint(1,500)
            message = Item(rand1,rand2)
            data_string = pickle.dumps(message)
            client_socket.send(data_string)
            Logger.Log(logMessage1)

            time.sleep(2)

    def  SendState(self):
        client_socket2 = self.CreateClientSocket2()
        while True:
            msg = self.inputState()
            client_socket2.send(msg.encode("utf-8"))
            Logger.Log(logMessage2)

    #zastita unosa stanja workera
    def inputState(self):
        try:
            state = input("Upisi broj za komandu koju zelite:\n\
                1.Upali novi worker\n\
                2.Ugasi workera\n\n")
            if state == "1":
                print("Upali workera")
                msg = "ON"
                return msg
            elif state == "2":
                print("Ugasi workera")
                msg = "OFF"
                return msg
            else: 
                #print("Molim Vas unesite samo broj 1 ili 2\n")
                self.inputState()
        except EOFError as e:
            print(e)   
if __name__ == "__main__":  # ovo ispod se nece pozvati pri importovanju
    writer = Writer()
    pItemSend = Process(target=writer.SendItem)
    tStateSend = threading.Thread(target=writer.SendState)
    pItemSend.start()
    tStateSend.start()
