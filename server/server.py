import zmq
import sys
import json
import os

context = zmq.Context()
socket = context.socket(zmq.REP)
port = sys.argv[1]
socket.bind(f"tcp://*:{port}")

server_info = {}


def createFolderIfNotExist():
    server_folder = sys.argv[2]
    if not os.path.isdir(server_folder):
        os.mkdir(server_folder)
    


def decideCommands():
    pass

def main():
    createFolderIfNotExist()
    print(f"server is running on port {port}")
    while True:
        request = socket.recv_multipart()
        socket.send(b'hola')
    return
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nserver closed") 