# Koristi Workere da bi citao podatke iz baze
import socket,pickle
import sys

sys.path.append('D:\GITHUB\RESProjekat3\RES-2022')
import worker
from multiprocessing import Process
from threading import Timer
from threading import Thread
from components.load_balancer import brojIstorijeWorkera, listaAktivnihWorkera

class Reader:

    workerLista = listaAktivnihWorkera
    pomBrWorkera = brojIstorijeWorkera
    client_host = '127.0.0.7'
    client_port = 6000
    client_socket = socket.socket()

    server_host = '127.0.1.1'
    server_port = 5002
    server_socket = socket.socket()

    brojacAktivnihWorkera= len(workerLista)

    def DoReader():
        print("test1")
        if Reader.pomBrWorkera > Reader.brojacAktivnihWorkera: #onda se smanjio broj workera   
                
                Reader.client_host = Reader.client_host[:-1] + ("% s" % (Reader.brojacAktivnihWorkera-1)) # ili str(brojacProcesa)  ISPRAVI KAD ODUZIMAS I DODAJES
                Reader.client_port = Reader.client_port - Reader.brojacAktivnihWorkera
                Reader.server_host = Reader.server_host[:-1] + ("% s" % (Reader.brojacAktivnihWorkera-1))
                Reader.server_port = Reader.server_port - Reader.brojacAktivnihWorkera
                tRequestCode.start()
                pReceiveData.start()
                

        else:
            x = 0
            while x < Reader.brojacAktivnihWorkera:
                    
                    Reader.client_host = Reader.client_host[:-1] + ("% s" % Reader.brojacAktivnihWorkera) # ili str(brojacProcesa)
                    Reader.client_port = Reader.client_port + Reader.brojacAktivnihWorkera
                    Reader.server_host = Reader.server_host[:-1] + ("% s" % Reader.brojacAktivnihWorkera)
                    Reader.server_port = Reader.server_port + Reader.brojacAktivnihWorkera
                    tRequestCode.start()
                    pReceiveData.start()
                    x+=1

            

    def ReceiveData():
        #Receives item
        print("RECEIVE DATA")
        Reader.server_socket.bind((Reader.server_host, Reader.server_port))
        Reader.server_socket.listen()
        conn, address = Reader.server_socket.accept()
        while True:
            dataRecv = conn.recv(4096)
            # receive data stream
            data = pickle.loads(dataRecv)
            if not data:
                # if data is not received break
                break
            print(data)
        conn.close()  # close the connection

    
    def EmprtyMessage():
        msg = ""
        Reader.client_socket.send(msg.encode("utf-8"))


    def  RequestCode():
        Reader.client_socket.connect((Reader.client_host, Reader.client_port)) 
        print("REQUEST CODE")
        while True:
            try:
                t = Timer(5.0, Reader.EmprtyMessage)
                t.start()
                t.join()
                state = input("Upisi broj za CODE koju zelite:\n\
                                1.ANALOG/DIGITAL\n\
                                2.CUSTOM/LIMITSET\n\
                                3.SINGLENODE/MULTIPLENODE\n\
                                4.CONSUMER/SOURCE\n")
                t.cancel()
                if state == "1":
                    print("ANALOG/DIGITAL")
                    msg = "1"
                if state == "2":
                    print("CUSTOM/LIMITSET")
                    msg = "2"
                if state == "3":
                    print("SINGLENODE/MULTIPLENODE")
                    msg = "3"
                if state == "4":
                    print("CONSUMER/SOURCE")
                    msg = "4"
                Reader.client_socket.send(msg.encode("utf-8"))
            except EOFError as e:
                print(e)


pReceiveData = Process(target=Reader.ReceiveData)
tRequestCode = Thread(target=Reader.RequestCode)

pDoReader = Process(target=Reader.DoReader)
pDoReader.start()