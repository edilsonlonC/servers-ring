from hashlib import sha1


def generateserverID(port, address):
    addressAndPort = port + address
    serverHash = sha1(addressAndPort.encode("utf-8")).hexdigest()
    serverID = int(serverHash, 16)
    return port
