import logging
import os
import platform
import socket
import sys


BASE_DIR = os.path.dirname(__file__)
LIB_DIR = os.path.join(BASE_DIR, 'lib')
ARCH = 'x64' if '64bit' in platform.architecture() else 'x86'
sys.path.insert(0, os.path.join(LIB_DIR))
sys.path.insert(0, os.path.join(LIB_DIR, ARCH))


import Leap
from Leap import Finger

from packets import Packet


logging.basicConfig(level='DEBUG')
logger = logging.getLogger(__file__)


class Listener(Leap.Listener):
    GRABBED = 20

    def __init__(self, port):
        super(Listener, self).__init__()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', port))
        s.listen(1)
        self.connection, address = s.accept()

    def on_init(self, controller):
        logger.info('Initialized')

    def on_connect(self, controller):
        logger.info('Connected')

    def on_disconnect(self, controller):
        logger.info('Disconnected')

    def on_exit(self, controller):
        logger.info('Exited')

    def on_frame(self, controller):
        packet = self.get_response(controller)
        print packet
        self.connection.sendall(packet.pack())

    @classmethod
    def listen(cls, port):
        controller = Leap.Controller()
        listener = cls(port)
        controller.add_listener(listener)
        try:
            sys.stdin.read()
        except KeyboardInterrupt:
            controller.remove_listener(listener)
            listener.connection.close()

    def get_response(self, controller):
        frame = controller.frame()
        packet = Packet.reset()
        for hand in frame.hands:
            if hand.is_left and self.is_grabbed(hand):
                packet = packet._replace(lhpp=hand.palm_position.to_tuple())
            elif hand.is_right:
                packet = packet._replace(rhpp=hand.palm_position.to_tuple())
                for finger in hand.fingers:
                    if finger.type() == Finger.TYPE_THUMB:
                        packet = packet._replace(rtf=finger.joint_position(Finger.JOINT_TIP).to_tuple())
                    elif finger.type() == Finger.TYPE_INDEX:
                        packet = packet._replace(rif=finger.joint_position(Finger.JOINT_TIP).to_tuple())
        return packet

    def is_grabbed(self, hand):
        fingers = list(hand.fingers)
        positions = (f.joint_position(Finger.JOINT_TIP) for f in fingers)
        thumb = next(positions)
        distances = (thumb.distance_to(finger) for finger in positions)
        return min(distances) < self.GRABBED


if __name__ == '__main__':
    Listener.listen(9050)
