"""Helper for feeding the Database with satellite position

Set up a UDP server that receive json objects, ans send them to the REST API
"""

import json
import socket

import requests

from core.config import Settings

satID = Settings.SATELLITES_ID

bufferSize  = 1024

# Cohoma server
ihmIP = "127.0.0.1"
ihmPort = 8000
# UDP server for rid_capture
localIP = "127.0.0.1"
localPort = 32001
# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
 
print("UDP server up and listening")

URL_IHM = f"http://{ihmIP}:{ihmPort}/api/waypoint/"
header = {'accept': 'application/json'}

while (True):
    try:
        session = requests.Session()

        # Listen for incoming datagrams
        while(True):
            bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
            message = bytesAddressPair[0].strip()
            address = bytesAddressPair[1]

            try:
                droneid = json.loads(message)
            except json.decoder.JSONDecodeError as e:
                print(f"Error: {message}")
                continue
            keys = droneid.keys()

            if 'debug' in keys:
                clientMsg = f"Heartbeat from {address}: {droneid}"

            elif 'uav id' in keys:
                uav = droneid["uav id"]
                if uav in satID.keys() :
                    clientMsg = f"Uav:{droneid}"
                    print(clientMsg)
                    data = {
                        'waypoint': satID[uav],
                        'lng': droneid['uav longitude'],
                        'lat': droneid['uav latitude']
                            }
                    result = session.post(URL_IHM, json=data)
                    if result.status_code != requests.codes.ok:
                        print(result.text)

    except Exception as e:
        print("exception!", e)
