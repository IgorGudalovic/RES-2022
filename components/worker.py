from ast import List
from logging import exception
import os
import sqlite3
import socket
import pickle
import threading
import time

import sys
sys.path.append('/home/x/Documents/GitHub/RES-2022/')
from constants.codes import Code
from constants.data_sets import DataSet, DataSets
from constants.queries import Queries
from models.collection_description import CollectionDescription
from models.description import Description
from models.worker_property import WorkerProperty
from multiprocessing import Process

client_socket = socket.socket() 
server_socket = socket.socket()

class Worker:
    def __init__(self, id: int, status=False, is_available=True):
        self.id = id
        self.status = status
        self.is_available = is_available  # Is False while worker is processing data
        self.collection_descriptions = [
            CollectionDescription(0, DataSet.DataSet_1, []),
            CollectionDescription(1, DataSet.DataSet_2, []),
            CollectionDescription(2, DataSet.DataSet_3, []),
            CollectionDescription(3, DataSet.DataSet_4, [])
        ]
        self.worker_properties_to_remove = {}

    # Method for saving data
    def SaveData(self, data: Description):
        if not self.is_available or not self.status:
            # If worker is off or busy
            return

        self.is_available = False
        self.__SaveLocally(data)
        cd_statuses = self.__EvaluateDataState()
        self.__ProcessData(cd_statuses)
        self.__RemoveCheckedWorkerProperties()
        self.is_available = True
        Worker.ReaderWorker(self)   #prima zahtev od readera i salje podatke


    # Parse data into local data structure
    def __SaveLocally(self, data: Description):
        dataset_id = DataSets[data.dataset]
        for item in data.items:
            worker_property = WorkerProperty(item.code, item.value)
            self.collection_descriptions[dataset_id].historical_collection.append(worker_property)

    def __EvaluateDataState(self):
        cd_statuses = []
        for cd in self.collection_descriptions:
            code_1, code_2 = False, False
            for worker_property in cd.historical_collection:
                if worker_property.code.name == cd.dataset.value[0]:
                    code_1 = True
                elif worker_property.code.name == cd.dataset.value[1]:
                    code_2 = True

            if code_1 and code_2:
                cd_statuses.append(True)
            else:
                cd_statuses.append(False)
        return cd_statuses

    def __ProcessData(self, cd_statuses: List):
        for cd, is_ready in zip(self.collection_descriptions, cd_statuses):
            if is_ready:
                for worker_property in cd.historical_collection:
                    if self.__ValidateValue(worker_property):
                        Worker.__SaveDataInDatabase(worker_property, cd.id)
                    else:
                        self.worker_properties_to_remove[cd.id] = worker_property

    @staticmethod
    def __SaveDataInDatabase(worker_property: WorkerProperty, dataset_id: int):
        db_path = Worker.__GetDatabasePath()
        with threading.Lock(), sqlite3.connect(db_path) as con:
            cur = con.cursor()
            query = Queries.InsertItem(dataset_id + 1, worker_property.code.name, worker_property.worker_value)
            cur.execute(query)
            con.commit()

    def __RemoveCheckedWorkerProperties(self):
        for cd_id, worker_property in self.worker_properties_to_remove.items():
            self.collection_descriptions[cd_id].historical_collection.remove(worker_property)
        self.worker_properties_to_remove.clear()

    def __ValidateValue(self, worker_property: WorkerProperty):
        if worker_property.code == Code.CODE_DIGITAL:
            return True

        last_value = self.__GetLastValueByCode(worker_property.code.name)
        if not last_value:  # No data in database with this code
            return True

        new_value = worker_property.worker_value
        return Worker.__CheckDeadband(last_value, new_value)

    def __GetLastValueByCode(self, code: str):
        try:
            return self.__GetValue(code)
        except sqlite3.OperationalError:
            self.__CreateDatabaseTables()
            return self.__GetLastValueByCode(code)

    def __GetValue(self, code: str):
        db_path = Worker.__GetDatabasePath()
        with threading.Lock(), sqlite3.connect(db_path) as con:
            cur = con.cursor()
            dataset_id = self.__GetDataSetByCode(code)
            query = Queries.GetLastValue(dataset_id + 1, code)
            cur.execute(query)
            record = cur.fetchone()

        if record is not None:
            record = record[0]
        return record

    @staticmethod
    def __CreateDatabaseTables():
        db_path = Worker.__GetDatabasePath()
        with threading.Lock(), sqlite3.connect(db_path) as con:
            cur = con.cursor()
            for dataset_id in range(1, 5):
                query = Queries.CreateDatasetTableQuery(dataset_id)
                cur.execute(query)

    @staticmethod
    def __GetDatabasePath():
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir[0:-11], "database\database.db")

    @staticmethod
    def __CheckDeadband(old_value, new_value):
        difference = abs(old_value - new_value)
        if difference > (old_value * 0.02):
            return True
        return False

    def __GetDataSetByCode(self, code: str):
        for id in range(0, 4):
            if code == self.collection_descriptions[id].dataset.value[0] or code == \
                    self.collection_descriptions[id].dataset.value[1]:
                return id

    def ChangeState(self, new_state: bool = None):
        if new_state is None:
            self.status = not self.status
        else:
            self.status = new_state

    def __str__(self):
        return f'Worker {self.id}: ({"On" if self.status else "Off"}, {"Fr__GetLastValueByCodeee" if self.is_available else "Busy"})'

    def ConnectClientSocket(self):
        global client_socket
        wID = self.id
        #wID+=1
        client_host = '127.0.2.' + (str(wID))
        client_port = 6001 + wID
        print(client_host, client_port )
        
        
        try:
            client_socket.connect((client_host, client_port))
        except socket.error as e:
            print()
            print("NECE DA SE KONETUJE")

    def ConnectServerSocket(self):
        global server_socket
        wID = self.id
        server_host = '127.0.0.' + (str(6 + wID))
        server_port = 5999 + self.id
        server_socket.bind((server_host, server_port))
        server_socket.listen()

    def ReceiveRequest(self):
        conn, address = server_socket.accept()
        pomBr = 0
        while True:
            try:
                dataRecv = conn.recv(4096).decode("utf-8")
                # receive data stream
                poruka = "Print Na WORKERU"
                if pomBr == 0:
                    pomBr+=1
                    Worker.ConnectClientSocket(self)
                if dataRecv == "1":
                    data_string = pickle.dumps(poruka)
                    client_socket.send(data_string)
                elif dataRecv == "2":                
                    data_string = pickle.dumps(poruka)
                    client_socket.send(data_string)
                elif dataRecv == "3":                
                    data_string = pickle.dumps(poruka)
                    client_socket.send(data_string)
                elif dataRecv == "4":
                    data_string = pickle.dumps(poruka)
                    client_socket.send(data_string)
                else:
                    data_string = pickle.dumps("NEMA DATA")
                    client_socket.send(data_string)
            except:
                data_string = pickle.dumps("GRESKA")
                client_socket.send(data_string)
                break
        conn.close()  # close the connection

    def ReaderWorker(self):
        Worker.ConnectServerSocket(self)
        pReceiveRequest = Process(target=Worker.ReceiveRequest(self))
        pReceiveRequest.start()
        