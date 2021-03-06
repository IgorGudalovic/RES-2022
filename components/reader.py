import socket,pickle
import sys
sys.path.append('/home/x/Documents/GitHub/RES-2022/')
from multiprocessing import Process
from threading import Thread
import load_balancer
from models.historical_value import HistoricalValue
from models.request import Request
from datetime import datetime

iterator = 0
pomBr = 0


class Reader:
    client_host = '127.0.0.7'
    client_port = 5999

    server_host = '127.0.1.1'
    server_port = 5001

    pomBrWorkera = getattr(load_balancer,'brojIstorijeWorkera')
    brojacAktivnihWorkera = getattr(load_balancer,'brWorkera')
    @staticmethod
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
    @staticmethod
    def CreateServerSocket():
        try:            
            server_socket = socket.socket()
            server_socket.bind((Reader.server_host, Reader.server_port))
            server_socket.listen()
            conn, address = server_socket.accept()
            return conn
        except:
            exit()
    @staticmethod
    def CreateClientSocket():
        try:
            client_socket = socket.socket()
            client_socket.connect((Reader.client_host, Reader.client_port))
            return client_socket
        except:
            exit()
    @staticmethod
    def ReceiveData():
        conn = Reader.CreateServerSocket()
        while True:
            try:
                dataRecv = conn.recv(4096)
                data = pickle.loads(dataRecv)
                print("Vrednost je:")
                print(data)
                if not data:
                    # if data is not received break
                    break
            except:
                print("Greska!!!!!!!!!!!")
        conn.close()
    @staticmethod
    def  RequestCode():
        global pomBr
        if pomBr==0:
            client_socket = Reader.CreateClientSocket()
            pomBr+=1
            reader = Reader()
        while True:
            msg = pickle.dumps(reader.optionInput())

            client_socket.send(msg)
            print("poslao requset")

    #zastita unosa za biranje requesta
    def optionInput(self):
        print("Upisi broj za opciju po kojoj zelite da nadjete vrednost:")
        print("1.Historical")#po vremenskom intervalu
        print("2.Code")#po kodu
        meni = input()
        if meni == "1":
            code = self.codeSelectionFunction()
            if code == "1":
                code = "CODE_ANALOG"
            if code == "2":
                code = "CODE_CUSTOM"
            if code == "3":
                code = "CODE_SINGLENOE"
            if code == "4":
                code = "CODE_CONSUMER"
            timeFrom = self.timeFromFunction()
            timeTo = self.timeToFunction()
            
            hv = HistoricalValue(timeFrom,timeTo,code)
            req = Request("Historical", hv)
            return req
        if meni == "2":
            code = self.codeSelectionFunction()
            if code == "1":
                code = "DataSet_1"
            if code == "2":
                code = "DataSet_2"
            if code == "3":
                code = "DataSet_3"
            if code == "4":
                code = "DataSet_4"

            req = Request("Code", code)
            return req
        else:
            print("Molim Vas unesite broj 1 ili 2")
            self.optionInput()

    #zastita unosa za code
    def codeSelectionFunction(self):
        code = input("Upisi broj za CODE koju zelite:\n\
                1.ANALOG/DIGITAL\n\
                2.CUSTOM/LIMITSET\n\
                3.SINGLENODE/MULTIPLENODE\n\
                4.CONSUMER/SOURCE\n")
        if code!="1" and code!="2" and code!="3" and code!="4":
            self.codeSelectionFunction()
        return code
    #zastita unosa za vreme1
    def timeFromFunction(self):
        timeFrom = input("Unesi vremenski interval u formatu Y-m-d H:M:S \nod:")
        try:
            date = datetime.strptime(timeFrom, '%Y-%m-%d %H:%M:%S')
            return date
        except:
            print("greska")
            self.timeFromFunction()

    #zastita unosa za vreme2
    def timeToFunction(self):
        timeTo = input("do:")
        try:
            date = datetime.strptime(timeTo, '%Y-%m-%d %H:%M:%S')
            return date
        except:
            print("greska")
            self.timeToFunction()

if __name__ == "__main__":  # ovo ispod se nece pozvati pri importovanju
    reader = Reader()
    pReceiveData = Process(target=reader.ReceiveData)
    tRequestCode = Thread(target=reader.RequestCode)
    reader.DoReader()
    pReceiveData.start()
    tRequestCode.start()
    while True:
        reader.DoReader()