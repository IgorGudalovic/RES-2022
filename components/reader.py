# Koristi Workere da bi citao podatke iz baze
import socket,pickle
import sys
import time
sys.path.append('/home/x/Documents/GitHub/RES-2022/')
from multiprocessing import Process
from threading import Timer
from threading import Thread
import load_balancer

iterator = 0

class Reader:
    pomBrWorkera = getattr(load_balancer,'brojIstorijeWorkera')
    client_host = '127.0.0.7'
    client_port = 5999


    server_host = '127.0.1.1'
    server_port = 5001

    brojacAktivnihWorkera = getattr(load_balancer,'brWorkera')
    def DoReader(): 
        if Reader.pomBrWorkera > Reader.brojacAktivnihWorkera: #onda se smanjio broj workera   
                Reader.client_host = Reader.client_host[:-1] + ("% s" % (Reader.brojacAktivnihWorkera-1)) # ili str(brojacProcesa)  ISPRAVI KAD ODUZIMAS I DODAJES
                Reader.client_port = Reader.client_port - Reader.brojacAktivnihWorkera
                Reader.server_host = Reader.server_host[:-1] + ("% s" % (Reader.brojacAktivnihWorkera-1))
                Reader.server_port = Reader.server_port - Reader.brojacAktivnihWorkera              

        else:
            global iterator
            while iterator < Reader.brojacAktivnihWorkera:
                    Reader.client_host = Reader.client_host[:-1] + ("% s" % (Reader.brojacAktivnihWorkera + 6)) # ili str(brojacProcesa)
                    Reader.client_port = Reader.client_port + Reader.brojacAktivnihWorkera
                    Reader.server_host = Reader.server_host[:-1] + ("% s" % Reader.brojacAktivnihWorkera)
                    Reader.server_port = Reader.server_port + Reader.brojacAktivnihWorkera
                    # print(Reader.client_host)
                    # print(Reader.client_port)
                    # print(Reader.server_host)
                    # print(Reader.server_port)
                    iterator+=1


            

    def ReceiveData():
        #Receives item
        server_socket = socket.socket()
        server_socket.bind((Reader.server_host, Reader.server_port))
        server_socket.listen()
        conn, address = server_socket.accept()
        while True:
            dataRecv = conn.recv(4096)
            # receive data stream
            try:
                data = pickle.loads(dataRecv)
                print(data)
            except:
                if not data:
                    # if data is not received break
                    break
        conn.close()  # close the connection

    
    def EmprtyMessage():
        print("")

    def  RequestCode():
        client_socket = socket.socket()
        client_socket.connect((Reader.client_host, Reader.client_port))  
        while True:
            print("CHOOSE CODE")
            try:
                t = Timer(2.0, Reader.EmprtyMessage)
                t.start()
                t.join()
                code = input("Upisi broj za CODE koju zelite:\n\
                    1.ANALOG/DIGITAL\n\
                    2.CUSTOM/LIMITSET\n\
                    3.SINGLENODE/MULTIPLENODE\n\
                    4.CONSUMER/SOURCE\n")
                t.cancel()
                if code == "1":
                    print("ANALOG/DIGITAL")
                    msg = "1"
                elif code == "2":
                    print("CUSTOM/LIMITSET")
                    msg = "2"
                elif code == "3":
                    print("SINGLENODE/MULTIPLENODE")
                    msg = "3"
                elif code == "4":
                    print("CONSUMER/SOURCE")
                    msg = "4"
                elif code!= "":
                    print("Molim Vas unesite samo broj 1 ili 2\n")
                client_socket.send(msg.encode("utf-8"))
                print("poslao")
                time.sleep(1)
            except EOFError as e:
                print("")


pReceiveData = Process(target=Reader.ReceiveData)
tRequestCode = Thread(target=Reader.RequestCode)
Reader.DoReader()
pReceiveData.start()
tRequestCode.start()
while True:
    time.sleep(2)
    Reader.DoReader()