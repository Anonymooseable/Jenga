import socket
from packets import Packet


class Receiver(object):
    def __init__(self, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('', port))
        self.socket.setblocking(False)
        self.buffer = b""

    def __iter__(self):
        return self

    def next(self):
        return self.__next__()

    def __next__(self):
        if len(self.buffer) < 8*12:
            self.buffer += self.socket.recv(1024)
        if len(self.buffer) >= 8*12:
            packetdata = self.buffer[:8*12]
            self.buffer = self.buffer[8*12:]
            return Packet.unpack(packetdata)

    def __del__(self):
        self.socket.close()
