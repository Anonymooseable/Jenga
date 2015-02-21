import logging
import os
import platform
import socket
from struct import pack
import sys


BASE_DIR = os.path.dirname(__file__)
LIB_DIR = os.path.join(BASE_DIR, 'lib')
ARCH = 'x64' if '64bit' in platform.architecture() else 'x86'
sys.path.insert(0, os.path.join(LIB_DIR))
sys.path.insert(0, os.path.join(LIB_DIR, ARCH))


import Leap


logging.basicConfig(level='DEBUG')
logger = logging.getLogger(__file__)


class Listener(Leap.Listener):
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
        response = self.get_response(controller)
        if response:
            packed = self.to_struct(response)
            print packed
            self.connection.sendall(packed)

    def to_struct(self, vector):
        return pack('ddd', vector.x, vector.y, vector.z)

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


class CameraListener(Listener):
    GRABBED = 20

    def get_response(self, controller):
        frame = controller.frame()
        for hand in frame.hands:
            if hand.is_left and self.is_grabbed(hand):
                return hand.palm_position

    def is_grabbed(self, hand):
        fingers = list(hand.fingers)
        positions = (f.joint_position(Leap.Finger.JOINT_TIP) for f in fingers)
        thumb = next(positions)
        distances = (thumb.distance_to(finger) for finger in positions)
        return min(distances) < self.GRABBED


class HandListener(Listener):
    def get_response(self, controller):
        frame = controller.frame()
        for hand in frame.hands:
            if hand.is_right:
                return hand.palm_position


if __name__ == '__main__':
    CameraListener.listen(9000)
