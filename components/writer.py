import sys
sys.path.append('/home/x/Documents/GitHub/RES-2022/')
import socket, pickle, time, random
import constants.codes as codes
from models.item import Item

#salje worker state
client_socket = socket.socket()
client_socket.connect((socket.gethostname(), 5001))
workerList = []
workerList.append("ON")
workerList.append("ON")
workerList.append("OFF")
workerList.append("ON")
message = workerList
print(f"List stanja je: {workerList}")
data_string = pickle.dumps(message)
client_socket.send(data_string)  

#salje item
listCodes = []
for code in codes.Code:
    listCodes.append(code.name)
while True:    
    rand1 = random.choice(listCodes)
    rand2 = random.randint(1,500)
    message = Item(rand1,rand2)
    print(f"Random1 je: {rand1}     Random2 je: {rand2}")
    data_string = pickle.dumps(message)
    client_socket.send(data_string)
    time.sleep(2)    