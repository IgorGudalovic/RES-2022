# Koristi Workere da bi citao podatke iz baze
import socket,pickle
import sys
import time
sys.path.append('D:/GITHUB/RESProjekat3/RES-2022')
from multiprocessing import Process
from threading import Thread
import load_balancer
from models.historical_value import HistoricalValue
from models.request import Request
from datetime import datetime

iterator = 0
pomBr = 0


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
                print("Vrednost je:")
                print(data)
            except:
                if not data:
                    # if data is not received break
                    break
        conn.close()  # close the connection


    def RequestCode():
        global pomBr
        if pomBr==0:
            client_socket = socket.socket()
            client_socket.connect((Reader.client_host, Reader.client_port))
            pomBr+=1
        while True:
            print("Upisi broj za opciju po kojoj zelite da nadjete vrednost:")
            print("1.Historical")#po vremenskom intervalu
            print("2.Code")#po kodu
            meni = input()
            if meni == "1":
                code = Reader.codeSelectionFunction()
                timeFrom = Reader.timeFromFunction ()
                timeTo = Reader.timeToFunction()
                
                hv = HistoricalValue(timeFrom,timeTo,code)
                req = Request("Historical", hv)
                msg = pickle.dumps(req)
            if meni == "2":
                code = Reader.codeSelectionFunction()
                req = Request("Code", code)
                msg = pickle.dumps(req)
            else:
                Reader.RequestCode
            client_socket.send(msg)
            print("poslao")
            time.sleep(1)

    #zastita unosa za code
    def codeSelectionFunction():
        code = input("Upisi broj za CODE koju zelite:\n\
                1.ANALOG/DIGITAL\n\
                2.CUSTOM/LIMITSET\n\
                3.SINGLENODE/MULTIPLENODE\n\
                4.CONSUMER/SOURCE\n")
        if code!="1" and code!="2" and code!="3" and code!="4":
            Reader.codeSelectionFunction()
        return code
    #zastita unosa za vreme1
    
    def timeFromFunction():
        timeFrom = input("Unesi vremenski interval u formatu Y-m-d H:M:S \nod:")        
        try:
            date = datetime.strptime(timeFrom, '%Y-%m-%d %H:%M:%S')
            datenow = datetime.now()
            if(date>datenow):
                print("Datum mora biti takav da je prosao")
                Reader.timeFromFunction()
            if(date.year < datetime.now().year and date.month < datetime.now().month and date.day < datetime.now().day):
                print("Format nije ispravan")
                Reader.timeFromFunction()                                              
            return date
        except:
            print("greska")
            Reader.timeFromFunction()                    

    #zastita unosa za vreme2
    def timeToFunction():
        timeTo = input("do:")
        try:
            date = datetime.strptime(timeTo, '%Y-%m-%d %H:%M:%S')
            datenow = datetime.now()
            if(date>datenow):
                print("Datum mora biti takav da je prosao")
                Reader.timeFromFunction()
            if(date.year < datetime.now().year and date.month < datetime.now().month and date.day < datetime.now().day):
                print("Format nije ispravan")
                Reader.timeFromFunction() 
            return date
        except:
            print("greska")
            Reader.timeToFunction()


pReceiveData = Process(target=Reader.ReceiveData)
tRequestCode = Thread(target=Reader.RequestCode)
Reader.DoReader()
pReceiveData.start()
tRequestCode.start()
while True:
    time.sleep(2)
    Reader.DoReader()