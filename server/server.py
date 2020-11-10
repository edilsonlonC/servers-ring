#!/home/edilson/anaconda3/bin/python3.8

import zmq
import sys
import json
import os
import argparse
from utilities.utilities import (
    getFieldsDict,
    insertFieldsDict,
    printPrettyJson,
    insertFieldsNewDict,
    isInRange,
    makeDirIfNotExist,
    savePart
)
from serverhash.serverhash import generateserverID

n = 6
parser = argparse.ArgumentParser("server files")
parser.add_argument("-p", "--port", help="port where is runnig server")
parser.add_argument("-sc", "--serverconnect", help="Address to node for connect")
parser.add_argument("-a", "--address", help="address where server server is running")
parser.add_argument("-id", "--identifier", help="identifier for test")
args = parser.parse_args()
serverconnect = args.serverconnect
port = args.port
address = args.address
identifier = int(args.identifier)


def inRange(request):
    identifier = request.get("identifier")
    server_range = serverInfo.get("server_range")
    json_response_fields = getFieldsDict(
            serverInfo, "port", "address", "identifier", "server_range", "succ", "pred"
        )
    in_range = False
    # is the first node
    if isinstance(server_range[0], list):
        first_range = server_range[0]
        second_range = server_range[1]
       
       
        if identifier >= first_range[0] and identifier < first_range[1]:
            serverInfo["server_range"] = [identifier, serverInfo.get("identifier")]
            serverInfo['pred']  = request
            in_range = True

        elif identifier >= second_range[0] and identifier < second_range[1]:
            serverInfo["server_range"] = [
                [0, serverInfo.get("identifier")],
                [identifier, 2 ** n],
            ]
            serverInfo['pred'] = request
            in_range = True
        if serverInfo.get("identifier") == serverInfo.get("succ").get("identifier"):
            serverInfo["succ"] = request
            serverInfo["pred"] = request.copy()
        print(in_range)
        json_response = insertFieldsNewDict(
            json_response_fields, in_range=in_range, first_node = True
        )
        return json_response
    else:
        
        if identifier > server_range[0] and identifier <= server_range[1]:
            serverInfo['server_range'] = [identifier,serverInfo.get('identifier')]
            json_response = insertFieldsNewDict(json_response_fields,in_range = True)
            serverInfo['pred'] = request
            return json_response
    return getFieldsDict(serverInfo,'address','port','identifier','succ','pred')
        



def join_network(request):
    
    address_server_connect = serverconnect
    while True:
        _socket = context.socket(zmq.REQ)
        _socket.connect(f"tcp://{address_server_connect}")
        _socket.send_multipart([json.dumps(request).encode("utf-8")])
        response = _socket.recv_multipart()
        json_response = json.loads(response[0])
        if json_response.get("in_range"):
            if json_response.get("first_node"):
                server_identifier = serverInfo.get("identifier")
                response_identifier = json_response.get("identifier")
                pred = json_response.get("pred")
                succ = json_response.get("succ")
                if server_identifier < response_identifier:
                    serverInfo["server_range"] = [
                        [0, server_identifier],
                        [pred.get("identifier"), 2 ** n],
                    ]
                elif server_identifier > response_identifier:
                    serverInfo["server_range"] = [
                        pred.get('identifier'),
                        server_identifier,
                    ]
                if response_identifier == json_response.get("pred").get("identifier"):
                    succ_and_pred = getFieldsDict(
                        json_response, "identifier", "address", "port"
                    )
                    serverInfo["succ"] = succ_and_pred
                    serverInfo["pred"] = succ_and_pred.copy()
                    return
            
            pred = json_response.get('pred')
            succ = getFieldsDict(json_response,'identifier','address','port')
            serverInfo['pred'] = pred
            serverInfo['succ'] = getFieldsDict(json_response,'identifier','port','address')
            if not json_response.get('first_node'): 
                serverInfo['server_range'] = [pred.get('identifier'),serverInfo.get('identifier')]
            print('pred',pred)
            address_server_connect = f"{pred.get('address')}:{pred.get('port')}"
            new_socket = context.socket(zmq.REQ)
            new_socket.connect(f"tcp://{address_server_connect}")
            new_succ = getFieldsDict(serverInfo,'address','port','identifier')
            new_succ['command'] = 'new_succ'
            new_socket.send_multipart([json.dumps(new_succ).encode('utf-8')])
            response = new_socket.recv_multipart()
            print('response',response)
            return
            
        succ = json_response.get('succ')
        address_server_connect = f"{succ.get('address')}:{succ.get('port')}"
        print('address_server_connect',address_server_connect)


def first_server():
    server_range = [
        [0, serverInfo.get("identifier")],
        [serverInfo.get("identifier"), 2 ** n],
    ]
    return insertFieldsDict(
        serverInfo,
        identifier=identifier,
        succ={"port": port, "address": address, "identifier": identifier},
        pred={"port": port, "address": address, "identifier": identifier},
        server_range=server_range,
    )


# new server


        


def newServer(request):
    print("newserver")
    json_response = inRange(request)
    socket.send_multipart([json.dumps(json_response).encode("utf-8")])

#response for client
def upload(request,_bytes):
    file_identifier = request.get('idfile')
    print('bytes',_bytes)
    _range  = serverInfo.get('server_range')
    print(_range)
    response = getFieldsDict(serverInfo,'identifier','port','address','succ','pred')

    if isInRange(file_identifier,_range):
        savePart(serverInfo.get('identifier'),file_identifier,_bytes)
        response['part_saved'] = True



    socket.send_multipart([json.dumps(response).encode('utf-8')]) 


def decide_commands(request,**kwargs):
    command = request.get("command")
    del request['command']
    if command == "new_server":
        newServer(request)
    if command == 'new_succ':
        serverInfo['succ'] = request
        print('new succ here', request)
        socket.send_multipart([json.dumps({'succ_saved': True}).encode('utf-8')])
    if command == 'upload':
        upload(request,kwargs.get('file_bytes'))
        #socket.send_multipart([b'in upload in server' ]) 


def main():
    while True:
        print("serverInfo")
        #printPrettyJson(serverInfo)

        print(serverInfo)
        request = socket.recv_multipart()
        json_request = json.loads(request[0])
        if len(request) > 1:
            decide_commands(json_request,file_bytes = request[1])
        else:
            decide_commands(json_request)
        print('serverInfo', serverInfo)


if __name__ == "__main__":
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{port}")
    serverInfo = {}
    servetInfo = insertFieldsDict(
        serverInfo, port=port, address=address, identifier=identifier
    )
    makeDirIfNotExist(str(identifier))
    if not serverconnect:
        serverInfo = first_server()
        print(f"server is running on port {port}")
    else:
        request = insertFieldsNewDict(serverInfo, command="new_server")
        join_network(request)

    try:
        main()
    except KeyboardInterrupt:
        print("\nserver closed")
