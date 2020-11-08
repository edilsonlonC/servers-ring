#!/home/edilson/anaconda3/bin/python3.8

import zmq
import sys
import json
import os
import argparse
from utilities.utilities import getFieldsDict , insertFieldsDict ,printPrettyJson, insertFieldsNewDict
from serverhash.serverhash import generateserverID

n = 6
parser = argparse.ArgumentParser("server files")
parser.add_argument("-p", "--port", help="port where is runnig server")
parser.add_argument("-sc", "--serverconnect", help="Address to node for connect")
parser.add_argument("-a", "--address", help="address where server server is running")
parser.add_argument('-id','--identifier',help = 'identifier for test')
args = parser.parse_args()
serverconnect = args.serverconnect
port = args.port
address = args.address
identifier = args.identifier


def inRange(identifier):
    server_range = serverInfo.get('server_range')
    if not insi


def join_network(request):
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://{serverconnect}")
    socket.send_multipart([json.dumps(request).encode('utf-8')])
    response = socket.recv_multipart()
    print(response)
    printPrettyJson(request)
    return

def first_server():
    server_range = [[0,serverInfo.get('identifier')],[serverInfo.get('identifier'),2 ** n]]
    return insertFieldsDict(
            serverInfo,identifier = identifier, 
            succ = {'port':port,'address':address},
            pred = {'port':port,'address': address},server_range = server_range
            
            )


#new server 
def newServer(request):
    print('newserver')
    printPrettyJson(request)
    socket.send_multipart([b'hola'])


def decide_commands(request):
    command = request.get('command')
   
    if command == 'new_server':
        newServer(request)


def main():
    while True:
        print('serverInfo')
        printPrettyJson(serverInfo)
        request = socket.recv_multipart()
        json_request = json.loads(request[0])
        decide_commands(json_request)

if __name__ == "__main__":
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{port}")
    serverInfo ={}
    servetInfo = insertFieldsDict(serverInfo,port=port,address=address,identifier = identifier)
    if not serverconnect:
        serverInfo = first_server()
        print(f"server is running on port {port}")
    else:
        request = insertFieldsNewDict(serverInfo,command = 'new_server')
        join_network(request)
        
    try:
        main()
    except KeyboardInterrupt:
        print("\nserver closed")
