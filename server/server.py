#!/home/edilson/anaconda3/bin/python3.8

import zmq
import sys
import json
import os
import argparse
from serverhash.serverhash import generateserverID

context = zmq.Context()
socket = context.socket(zmq.REP)
parser = argparse.ArgumentParser('server files')
parser.add_argument('-p','--port',help='port where is runnig server')
parser.add_argument('-sc','--serverconnect',help='Address to node for connect')
parser.add_argument('-a','--address',help='address where server server is running')
args = parser.parse_args()
serverconnect = args.serverconnect
port = args.port
address = args.address
socket.bind(f"tcp://*:{port}")

serverInfo = {}


def generateInfoServer(serverId,address,port):
    serverInfo['address'] = address
    serverInfo['port'] = port
    serverInfo['serverId'] = serverId
    print(serverInfo)

def createFolderIfNotExist():
    server_folder = sys.argv[2]
    if not os.path.isdir(server_folder):
        os.mkdir(server_folder)
    
def networkConnect(serverConnect):
    _context = zmq.Context()
    _socket = _context.socket(zmq.REQ)
    _socket.connect(f"tcp://{serverConnect}")
    infoToSend = serverInfo
    infoToSend['command'] = 'newserver'
    _socket.send_multipart([json.dumps(infoToSend).encode('utf-8')])
    response = _socket.recv_multipart()
    response_json = json.loads(response[0])
    succFirtsNode = None
    print (response_json)
    if not response_json.get('succ'):
        serverInfo['succ'] = response_json
        succFirtsNode = serverInfo
        succFirtsNode['command'] = 'firstsucc'
        _socket.send_multipart([json.dumps(succFirtsNode).encode('utf-8')])
        response = _socket.recv_multipart()
        print(serverInfo)
        print(response)



def decideCommands(json_response):
    command = json_response.get('command')
    if command == 'newserver':
        socket.send_multipart([json.dumps(serverInfo).encode('utf-8')])
    elif command == 'firstsucc':
        del json_response['command']
        serverInfo['succ'] = json_response
        print(serverInfo)
        socket.send_multipart([json.dumps({'succSaved': True}).encode('utf-8')])
def main():
    createFolderIfNotExist()
    serverID = generateserverID(port,address) 
    generateInfoServer(serverID,address,port)
    if serverconnect:
        networkConnect(serverconnect)

    print(f"server is running on port {port}")
    while True:
        request = socket.recv_multipart()
        json_response = json.loads(request[0])
        decideCommands(json_response)
    return
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nserver closed") 