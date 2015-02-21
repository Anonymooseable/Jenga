import logging
import os
import platform
import sys


logger = logging.getLogger(__file__)


BASE_DIR = os.path.dirname(__file__)
LIB_DIR = os.path.join(BASE_DIR, 'lib')
ARCH = 'x64' if '64bit' in platform.architecture() else 'x86'
sys.path.insert(0, os.path.join(LIB_DIR))
sys.path.insert(0, os.path.join(LIB_DIR, ARCH))


import Leap


class HandListener(Leap.Listener):
    def on_init(self, controller):
        logger.info('Initialized')

    def on_connect(self, controller):
        logger.info('Connected')
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)

    def on_disconnect(self, controller):
        logger.info('Disconnected')

    def on_exit(self, controller):
        logger.info('Exited')

    @classmethod
    def listen(cls):
        controller = Leap.Controller()
        listener = cls()
        controller.add_listener(listener)
        try:
            sys.stdin.read()
        except KeyboardInterrupt:
            controller.remove_listener(listener)


class CameraController(HandListener):
    GRABBED = 20

    def on_frame(self, controller):
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


class HandController(HandListener):
    def on_frame(self, controller):
        frame = controller.frame()
        for hand in frame.hands:
            if hand.is_right:
                return hand.palm_position


if __name__ == "__main__":
    CameraController.listen()
