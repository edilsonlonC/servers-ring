#!/home/edilson/anaconda3/bin/python3.8


import zmq
import argparse
import json
from hashlib import sha256
from utilities.utilities import printPrettyJson, get_newname , file_exist, makedirIfNotExist
import fileinput

parser = argparse.ArgumentParser("Client files")
parser.add_argument("-f", "--filename", help="File name than you want upload")
parser.add_argument("-sc", "--serverconnect", help="address of server")
parser.add_argument(
    "-c", "--command", help="Command that you want execute: upload , download"
)
parser.add_argument("--hash", help="Hash file that you want download")
args = parser.parse_args()
filename = args.filename
serverconnect = args.serverconnect
command = args.command
chord_hash = args.hash

part_size = 1024 * 1024 * 10


def search_node_download(request):
    context = zmq.Context()
    address_server = serverconnect
    while True:
        socket = context.socket(zmq.REQ)
        socket.connect(f"tcp://{address_server}")
        socket.send_multipart([json.dumps(request).encode("utf-8")])
        response = socket.recv_multipart()
        if len(response) > 1:
            return {"bytes": response[1]}
        response_json = json.loads(response[0])
        if response_json.get("FileNotFoundError"):
            return response_json
        succ = response_json.get("succ")
        address_server = f"{succ.get('address')}:{succ.get('port')}"


def search_node(request, bytes_to_send):
    context = zmq.Context()
    address_server = serverconnect
    while True:
        socket = context.socket(zmq.REQ)
        socket.connect(f"tcp://{address_server}")
        socket.send_multipart([json.dumps(request).encode("utf-8"), bytes_to_send])
        response = socket.recv_multipart()
        response_json = json.loads(response[0])
        if response_json.get("part_saved"):
            print("part is saved in")
            printPrettyJson(response_json)
            return response_json
        succ = response_json.get("succ")
        address_server = f"{succ.get('address')}:{succ.get('port')}"


def insertCompleteHash(filename, completeHash):
    print("working en completeHash")


def getCompletehashChord(filename):
    # Error here, no return bytes
    try:
        _file_path = f"temp/{filename}.chord"
        _file_chord = open(_file_path, "rb+")
        _bytes = _file_chord.read()
        _hash = sha256(_bytes).hexdigest()
        return _hash, _bytes

    except FileNotFoundError:
        print(f"{filename}.chord doesn't exist")
        return


# no use
def createFchord(filename, hash_parts):
    _file_chord = open(f"temp/{filename}.chord", "w")
    _file_chord.writelines(hash_parts)
    return


def upload(request):
    filename = request.get("filename")
    # hash_parts = []
    try:

        _file = open(filename, "rb")
        _bytes = _file.read(part_size)
        _fileChord = open(f"temp/{filename}.chord", "w+")
        _fileChord.write(f"{filename}\n")
        _fileChord.write("#\n")
        while _bytes:
            part_hash = sha256(_bytes).hexdigest()
            request["hash_part"] = part_hash
            search_node(request, _bytes)
            # hash_parts.append(f"{part_hash}\n")
            _fileChord.write(f"{part_hash}\n")
            _bytes = _file.read(part_size)

        _fileChord.close()

        hash_complete_chord, _bytes_chord = getCompletehashChord(filename)
        print("complete hash", hash_complete_chord)
        request["hash_part"] = hash_complete_chord
        response_server = search_node(request, _bytes_chord)
        print("hash file chord : ", response_server["hash_saved"])
        print("identifier", int(response_server.get("hash_saved"), 16))

        # insertCompleteHash(filename,"Here is the complete hash")

    except FileNotFoundError:
        print(f"File {filename} doesn't exist")


def download_chord(request):
    response = search_node_download(request)
    _bytes = response.get("bytes")
    print(_bytes)
    if _bytes:
        _file = open("temp/f.chord", "w")
        _file.write(_bytes.decode("utf-8"))
        return True

    return False


def create_file(filename, _bytes):
    _file = open(filename, "ab")
    _file.write(_bytes)
    return


def download(request):
    is_download = download_chord(request)
    if is_download:
        print("lines file chord")
        # TODO: Send to server each hash of chord splited and send to create file
        try:
            _file = open("temp/f.chord", "r")
            line = _file.readline()  # file name
            filename = line.split("\n")[0]
            if file_exist(filename):
                filename = get_newname(filename)
            _file_download = open(f"{filename}", "ab")
            line = _file.readline()  # Complete hash
            while line:
                line = _file.readline()  # part hashes
                request["hash_part"] = line.split("\n")[0]
                if not line:
                    return
                response = search_node_download(request)
                _bytes = response.get("bytes")
                if _bytes:
                    _file_download.write(_bytes)

        except FileNotFoundError:
            print("error")
    return


#####################################################################################3
def decide_command(request):
    command = request.get("command")
    if command == "upload":
        print("upload here")
        upload(request)
    elif command == "download":
        download(request)
        return
    else:
        print(f"command {command} doesn't exist")


def main(): 
    request = {
        "filename": filename,
        "command": command,
    }
    if chord_hash:
        request["hash_part"] = chord_hash
    decide_command(request)
    return


if __name__ == "__main__":
    makedirIfNotExist('temp')
    print(filename, serverconnect)
    main()
