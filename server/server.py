#!/home/edilson/anaconda3/bin/python3.8

import zmq
import sys
import json
import os
import argparse
from serverhash.serverhash import generateserverID

n = 6
context = zmq.Context()
socket = context.socket(zmq.REP)
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
socket.bind(f"tcp://*:{port}")

serverInfo = {}


#new server command 

def newServer(json_request):
    request_serverId = json_request.get('serverId')
    server_range = serverInfo.get('range')
    if (not isinstance(server_range[0],list)):
        if (request_serverId > server_range[0] and request_serverId <= server_range[1]):
            serverInfo['store'] = True
            json_to_send = {}
            json_to_send['range'] = [server_range[0],request_serverId]
            serverInfo['range'] = [request_serverId,server_range[1]]
            json_to_send['store'] = True
            json_to_send['succ'] = True
            
            socket.send_multipart([json.dumps(json_to_send).encode('utf-8')])
            del serverInfo['store']
            return
        
    
    json_response = serverInfo.get('succ')
    json_response['store'] = False
    socket.send_multipart([json.dumps(json_response).encode('utf-8')])
    del json_response['store']

       
    
def generateInfoServer(serverId, address, port):
    serverInfo["address"] = address
    serverInfo["port"] = port
    serverInfo["serverId"] = serverId


def createFolderIfNotExist():
    server_folder = sys.argv[2]
    if not os.path.isdir(server_folder):
        os.mkdir(server_folder)

def findServerInrange(serverConnect):
    serverInfo['command'] = 'new_server'
    isServer = False
    _context = zmq.Context()
    _socket = _context.socket(zmq.REQ)
    while not isServer:
        _socket.connect(f"tcp://{serverConnect}")
        _socket.send_multipart([json.dumps(serverInfo).encode('utf-8')])
        response = _socket.recv_multipart()
        json_response = json.loads(response[0])
        isServer = json_response.get('store')
        responseAddress = json_response.get('address')
        port = json_response.get('port')
        serverConnect = f"{responseAddress}:{port}"
        print('is server' ,json_response)
    del json_response['store']
    return json_response

    return

def newNodeInNetwork(serverConnect):
    json_response = findServerInrange(serverConnect)
    serverInfo['succ'] = json_response.get('succ')
    serverInfo['range'] = json_response.get('range')

def networkConnect(serverConnect):
    _context = zmq.Context()
    _socket = _context.socket(zmq.REQ)
    _socket.connect(f"tcp://{serverConnect}")
    infoToSend = serverInfo
    infoToSend["command"] = "second_server"
    _socket.send_multipart([json.dumps(infoToSend).encode("utf-8")])
    response = _socket.recv_multipart()
    response_json = json.loads(response[0])
    succFirtsNode = dict()
    idServer = serverInfo.get("serverId")
    idServerConnected = response_json.get("serverId")
    if not response_json.get("succ"):
        serverInfo["succ"] = {}
        for key in response_json:
            serverInfo["succ"][key] = response_json[key]
        for key in serverInfo:
            succFirtsNode[key] = serverInfo[key]
        succFirtsNode["command"] = "firstsucc"
        if idServer > idServerConnected:
            serverInfo["range"] = [idServerConnected, idServer]
            succFirtsNode["range"] = [[idServer, 2 ** n], [0, idServerConnected]]
        else:
            succFirtsNode["range"] = [idServer, idServerConnected]
            serverInfo["range"] = [[idServerConnected, 2 ** n], [0, idServer]]
        _socket.send_multipart([json.dumps(succFirtsNode).encode("utf-8")])
        response = _socket.recv_multipart()
        del serverInfo["command"]


def firstSucc(jsonRequest):
    rangeServer = jsonRequest.get("range")
    del jsonRequest["range"]
    del jsonRequest["command"]
    serverInfo["range"] = rangeServer
    serverInfo["succ"] = jsonRequest
    socket.send_multipart([json.dumps({"succSaved": True}).encode("utf-8")])


def decideCommands(jsonRequest):
    command = jsonRequest.get("command")
    if command == "second_server":
        del jsonRequest['command']
        server_info['pre'] =  jsonRequest
        socket.send_multipart([json.dumps(serverInfo).encode("utf-8")])
    elif command == "firstsucc":
        firstSucc(jsonRequest)
    elif command == 'new_server':
        newServer(jsonRequest)


def main():
    #createFolderIfNotExist()
    if identifier:
        serverID = identifier
    else :
        serverID = generateserverID(port, address)
    generateInfoServer(serverID, address, port)
    if serverconnect:
        networkConnect(serverconnect)
    if not serverInfo.get('succ') and serverconnect:
        newNodeInNetwork(serverconnect)

    print(f"server is running on port {port}")
    while True:
        print(serverInfo)
        request = socket.recv_multipart()
        jsonRequest = json.loads(request[0])
        decideCommands(jsonRequest)
    return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nserver closed")
