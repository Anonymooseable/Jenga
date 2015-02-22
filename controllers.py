import socket
from packets import Packet


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
        except socket.error:
            self.socket.close()
        else:
            return Packet.unpack(data)


receiver = Receiver(9050)


def camera_controller(controller):
    for vector in iter(receiver):
        print(vector)


if __name__ == '__main__':
    camera_controller(1)
