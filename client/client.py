import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect('tcp://localhost:5555')




def main():
    socket.send_multipart([b'hola'])
    response = socket.recv()
    print(response)

if __name__ == '__main__':
    main()
    