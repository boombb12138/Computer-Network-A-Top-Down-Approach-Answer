# UDPPingerClient.py
from socket import *
import time
serverName = '127.0.0.1'
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_DGRAM)

sequence_number = 0;# 序列号
while True:
    try:
        time1 = time.time()
        outputdata =  f'Heartbeat {sequence_number} {time1}'
        clientSocket.sendto(outputdata.encode(), (serverName, serverPort))
        sequence_number+=1
        time.sleep(10)
    except KeyboardInterrupt:
        print("Heartbeat Client is closed")
        break
clientSocket.close()
