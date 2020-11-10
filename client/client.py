#!/home/edilson/anaconda3/bin/python3.8


import zmq
import argparse
import json
from utilities.utilities import printPrettyJson

parser = argparse.ArgumentParser("Client files")
parser.add_argument("-f", "--filename", help="File name than you want upload")
parser.add_argument("-sc", "--serverconnect", help="address of server")
parser.add_argument("-id", "--idfile", help="id file only for test")
parser.add_argument(
    "-c", "--command", help="Command that you want execute: upload , download"
)
args = parser.parse_args()
filename = args.filename
serverconnect = args.serverconnect
idfile = int(args.idfile)
command = args.command

part_size = 1024 * 1024 
def search_node(request, bytes_to_send):
    context = zmq.Context()
    address_server = serverconnect
    while True:
        print(address_server)
        socket = context.socket(zmq.REQ)
        socket.connect(f"tcp://{address_server}")
        socket.send_multipart([json.dumps(request).encode("utf-8"), bytes_to_send])
        response = socket.recv_multipart()
        print("response")
        response_json = json.loads(response[0])
        if response_json.get("part_saved"):
            print("part is saved in")
            printPrettyJson(response_json)
            return
        succ = response_json.get("succ")
        address_server = f"{succ.get('address')}:{succ.get('port')}"


def decide_command(request):
    command = request.get("command")
    if command == "upload":
        print("upload here")
        search_node(request, b"testbytes")


def main():
    request = {
        "filename": filename,
        "command": command,
        "idfile": idfile,
    }
    decide_command(request)
    return


if __name__ == "__main__":
    print(filename, serverconnect, idfile)
    main()
