import socket
from .packets import Packet


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




def camera(controller):
    camera_receiver = Receiver(9000)
    print(dir(controller))
    for vector in iter(camera_receiver):
        print(vector)


def hand(controller):
    hand_receiver = Receiver(9001)
    for vector in iter(hand_receiver):
        print(vector)
