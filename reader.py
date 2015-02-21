import os
import platform
import sys
import logging

logger = logging.getLogger(__file__)

BASE_DIR = os.path.dirname(__file__)
LIB_DIR = os.path.join(BASE_DIR, 'lib')
ARCH = 'x64' if '64bit' in platform.architecture() else 'x86'
sys.path.insert(0, os.path.join(LIB_DIR))
sys.path.insert(0, os.path.join(LIB_DIR, ARCH))


import Leap


class HandListener(Leap.Listener):
    def __init__(self, camera, hand):
        super(HandListener, self).__init__()
        self.camera = camera
        self.hand = hand

    def on_init(self, controller):
        logger.info('Initialized')

    def on_connect(self, controller):
        logger.info('Connected')
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)

    def on_disconnect(self, controller):
        logger.info('Disconnected')

    def on_exit(self, controller):
        logger.info('Exited')

    def on_frame(self, controller):
        frame = controller.frame()
        for hand in frame.hands:
            if hand.is_left:
                self.camera.on_hand(hand)
            else:
                self.hand.on_hand(hand)


class CameraController(object):
    GRABBED = 20

    def on_hand(self, hand):
        if self.is_grabbed(hand):
            return hand.palm_position

    def is_grabbed(self, hand):
        fingers = list(hand.fingers)
        positions = (f.joint_position(Leap.Finger.JOINT_TIP) for f in fingers)
        thumb = next(positions)
        distances = (thumb.distance_to(finger) for finger in positions)
        return min(distances) < self.GRABBED


class HandController(object):
    def on_hand(self, hand):
        return hand.palm_position


def main():
    camera = CameraController()
    hand = HandController()
    listener = HandListener(camera, hand)
    controller = Leap.Controller()
    controller.add_listener(listener)

    try:
        sys.stdin.read()
    except KeyboardInterrupt:
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
