from distutils.log import error
from logging import exception
import sys
import threading
sys.path.append('D:\Res-2022')
import socket, pickle, time, random
import constants.codes as codes
from models.item import Item
from multiprocessing import Process
from threading import Timer

class Writer:
    
    def CreateClientSocket1():
        try:
            client_socket = socket.socket()
            client_socket.connect(('127.0.0.1', 5001))
            return client_socket
        except:
            exit()
        
    def CreateClientSocket2():
        try:
            client_socket2 = socket.socket()
            client_socket2.connect(('127.0.0.2', 5000))
            return client_socket2
        except:
            exit()

    def SendItem():
        client_socket = Writer.CreateClientSocket1()    
        listCodes = []
        for code in codes.Code:
            listCodes.append(code.name)
        while True:    
            rand1 = random.choice(listCodes)
            rand2 = random.randint(1,500)
            message = Item(rand1,rand2)
            data_string = pickle.dumps(message)
            client_socket.send(data_string)
            time.sleep(2)

    def SendState():
        client_socket2 = Writer.CreateClientSocket2()
        while True:
            msg = Writer.inputState()
            client_socket2.send(msg.encode("utf-8"))

    def inputState():
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
                print("Molim Vas unesite samo broj 1 ili 2\n")
                Writer.inputState()
        except EOFError as e:
            print(e)
            return None   

            
#LoadBalancer.DoLoadBalancer()
pItemSend = Process(target=Writer.SendItem)
tStateSend = threading.Thread(target=Writer.SendState)
pItemSend.start()
tStateSend.start()
