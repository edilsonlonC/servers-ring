from hashlib import sha256
from utilities.utilities import getRandomString


def generateServerID(port, address):
    addressAndPort = port + address + getRandomString(30)
    serverHash = sha256(addressAndPort.encode("utf-8")).hexdigest()
    serverID = int(serverHash, 16)
    return serverID
