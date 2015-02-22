import socket
from jenga.packets import Packet


class Receiver(object):
    def __init__(self, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('', port))

    def __iter__(self):
        return self

    def next(self):
        return self.__next__()

    def __next__(self):
        try:
            data = self.socket.recv(8 * 12)
        except Exception:
            self.socket.close()
        else:
            return Packet.unpack(data)
