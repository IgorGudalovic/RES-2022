import sys
import threading
sys.path.append('/home/x/Documents/GitHub/RES-2022/')
import socket, pickle, time, random
import constants.codes as codes
from models.item import Item
from multiprocessing import Process
from threading import Timer

client_socket = socket.socket()
client_socket.connect(('127.0.0.1', 5001))    
client_socket2 = socket.socket()
client_socket2.connect(('127.0.0.2', 5000)) 

class Writer:

    def SendItem():      
        listCodes = []
        for code in codes.Code:
            listCodes.append(code.name)
        while True:    
            rand1 = random.choice(listCodes)
            rand2 = random.randint(1,500)
           # print(rand1 , rand2)
            message = Item(rand1,rand2)
            data_string = pickle.dumps(message)
            client_socket.send(data_string)
            time.sleep(2)

    def EmprtyMessage():
        msg = ""
        client_socket2.send(msg.encode("utf-8"))

    def  SendState():   
        while True:
            try:
                t = Timer(2.0, Writer.EmprtyMessage)
                t.start()
                t.join()
                state = input("Upisi broj za komandu koju zelite:\n\
                    1.Upali novi worker\n\
                    2.Ugasi workera\n\n")
                t.cancel()
                if state == "1":
                    print("Upali workera")
                    msg = "ON"
                else:
                    if state == "2":
                        print("Ugasi workera")
                        msg = "OFF"
                    else: 
                        print("Molim Vas unesite samo broj 1 ili 2\n")
                client_socket2.send(msg.encode("utf-8"))
            except EOFError as e:
                print(e)            
            
#LoadBalancer.DoLoadBalancer()
pItemSend = Process(target=Writer.SendItem)
tStateSend = threading.Thread(target=Writer.SendState)
pItemSend.start()
tStateSend.start()
