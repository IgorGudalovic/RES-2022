import os
import sqlite3
import socket
import pickle
import threading
import sys
sys.path.append('/home/x/Documents/GitHub/RES-2022/')

from constants.codes import Code, Codes
from constants.data_sets import DataSet, DataSets
from constants.queries import Queries
from models.collection_description import CollectionDescription
from models.description import Description
from models.worker_property import WorkerProperty
from multiprocessing import Process
from datetime import datetime

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

    # Method used in reader to get all data for a specific code and timestamps
    # Method returns (timestamp(date), WorkerProperty(code, value))
    def GetData(self, code: str, db_path=None):
        if code not in Codes:
            return []

        dataset_id = self.GetDataSetByCode(code)
        if db_path is None:
            db_path = Worker.__GetDatabasePath()
        with threading.Lock(), sqlite3.connect(db_path) as con:
            cur = con.cursor()
            query = Queries.GetData(dataset_id + 1, code)
            cur.execute(query)
            records = cur.fetchall()

        data = []
        if records is not None:
            for record in records:
                date = datetime.strptime(record[0], '%Y-%m-%d %H:%M:%S')
                data.append((date, WorkerProperty(record[1], record[2])))

        return data

    # Method for saving data
    def SaveData(self, data: Description):  # pragma: no cover
        if not self.is_available or not self.status:
            # If worker is off or busy
            return

        self.is_available = False
        self.__SaveLocally(data)
        cd_statuses = self.__EvaluateDataState()
        self.__ProcessData(cd_statuses)
        self.__RemoveCheckedWorkerProperties()
        self.is_available = True

    def GetLastValueByCode(self, code: str, db_path=None):
        try:
            return self.GetValue(code, db_path)
        except sqlite3.OperationalError:
            self.__CreateDatabaseTables()
            return self.GetLastValueByCode(code)

    # Parse data into local data structure
    def __SaveLocally(self, data: Description):  # pragma: no cover
        dataset_id = DataSets.index(data.dataset.name)
        for item in data.items:
            worker_property = WorkerProperty(item.code, item.value)
            self.collection_descriptions[dataset_id].historical_collection.append(worker_property)

    # Check if any CollectionDescription is ready for saving in database
    def __EvaluateDataState(self):  # pragma: no cover
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

    # Process any ready CollectionDescriptions
    def __ProcessData(self, cd_statuses: list):  # pragma: no cover
        for cd, is_ready in zip(self.collection_descriptions, cd_statuses):
            if is_ready:
                for worker_property in cd.historical_collection:
                    if self.ValidateValue(worker_property):
                        Worker.__SaveDataInDatabase(worker_property, cd.id)
                    else:
                        self.worker_properties_to_remove[cd.id] = worker_property

    @staticmethod
    def __SaveDataInDatabase(worker_property: WorkerProperty, dataset_id: int, db_path=None):  # pragma: no cover
        if db_path is None:
            db_path = Worker.__GetDatabasePath()
        with threading.Lock(), sqlite3.connect(db_path) as con:
            cur = con.cursor()
            query = Queries.InsertItem(dataset_id + 1, worker_property.code.name, worker_property.worker_value)
            cur.execute(query)
            con.commit()

    # Remove processed data from worker
    def __RemoveCheckedWorkerProperties(self):  # pragma: no cover
        for cd_id, worker_property in self.worker_properties_to_remove.items():
            self.collection_descriptions[cd_id].historical_collection.remove(worker_property)
        self.worker_properties_to_remove.clear()

    # Check if data can be saved in database
    def ValidateValue(self, worker_property: WorkerProperty, db_path=None):
        if worker_property.code == Code.CODE_DIGITAL:
            return True

        last_value = self.GetLastValueByCode(worker_property.code.name, db_path)
        if not last_value:  # No data in database with this code
            return True

        new_value = worker_property.worker_value
        return Worker.CheckDeadband(last_value, new_value)

    def GetValue(self, code: str, db_path=None):
        if db_path is None:
            db_path = Worker.__GetDatabasePath()
        with threading.Lock(), sqlite3.connect(db_path) as con:
            cur = con.cursor()
            dataset_id = self.GetDataSetByCode(code)
            query = Queries.GetLastValue(dataset_id + 1, code)
            cur.execute(query)
            record = cur.fetchone()

        if record is not None:
            record = record[0]
        return record

    @staticmethod
    def __CreateDatabaseTables(db_path=None):  # pragma: no cover
        if db_path is None:
            db_path = Worker.__GetDatabasePath()
        with threading.Lock(), sqlite3.connect(db_path) as con:
            cur = con.cursor()
            for dataset_id in range(1, 5):
                query = Queries.CreateDatasetTableQuery(dataset_id)
                cur.execute(query)

    @staticmethod
    def __GetDatabasePath():  # pragma: no cover
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir[0:-11], "database\database.db")

    # Checks if new value is out of deadband of old value
    @staticmethod
    def CheckDeadband(old_value: int, new_value: int):
        difference = abs(old_value - new_value)
        if difference > (old_value * 0.02):
            return True
        return False

    def GetDataSetByCode(self, code: str):
        for id in range(0, 4):
            if code == self.collection_descriptions[id].dataset.value[0] or code == \
                    self.collection_descriptions[id].dataset.value[1]:
                return id

    def ChangeState(self, new_state: bool = None):  # pragma: no cover
        if new_state is None:
            self.status = not self.status
        else:
            self.status = new_state

    def __str__(self):  # pragma: no cover
        return f'Worker {self.id}: ({"On" if self.status else "Off"}, {"Free" if self.is_available else "Busy"})'

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
        server_port = 5999 + wID
        server_socket.bind((server_host, server_port))
        server_socket.listen()

    def ReceiveRequest(self):
        conn, address = server_socket.accept()
        pomBr = 0
        while True:
            try:
                dataRecv = pickle.loads(conn.recv(4096))# on primi objekat Request-a
                #prvi put kad primi request napravi klijenta za slanje na reader
                if pomBr == 0:
                    pomBr+=1
                    Worker.ConnectClientSocket(self)


                #dobavi value po vremenu
                #if data[0] == "Historical":
                
                #dobavi value po kodu
                #elif data[0] == "Code":

                #posalji dobavljen value
                #data_string = pickle.dumps(dataSend)
                #client_socket.send(data_string)
            except:
                data_string = pickle.dumps("GRESKA")
                client_socket.send(data_string)
                break
        conn.close()  # close the connection

    def ReaderWorker(self):
        Worker.ConnectServerSocket(self)
        pReceiveRequest = Process(target=Worker.ReceiveRequest(self))
        pReceiveRequest.start()
        