import sys
sys.path.append('/home/x/Documents/GitHub/RES-2022/')
import socket, pickle, time, random
import constants.codes as codes
from models.item import Item


client_socket = socket.socket()
client_socket.connect((socket.gethostname(), 5000))
listCodes = []
for code in codes.Code:
    listCodes.append(code.name)
workerList = []
workerList.append("ON")
workerList.append("ON")
workerList.append("OFF")
workerList.append("ON")
while True:    
    rand1 = random.choice(listCodes)
    rand2 = random.randint(1,500)
    dictRandValue = {rand1,rand2}
    message = Item(rand1,rand2)
    dict = {message, workerList}
    print(f"Random1 je: {rand1}     Random2 je: {rand2}")
    data_string = pickle.dumps(dict)
    client_socket.send(data_string)
    time.sleep(2)    