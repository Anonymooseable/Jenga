import bge

from jenga.receivers import Receiver


receiver = Receiver(9002)
previous = (0, 0, 0)


def camera(controller):
    try:
        scene = bge.logic.getCurrentScene()
        camera = scene.active_camera
        vector = next(receiver)[0]
        if previous is (0, 0, 0):
            return
        change = [v_a + p_a for v_a, p_a in zip(vector, previous)]
        change = [a*0.001 for a in change]
        position = [pos + axis for pos, axis in zip(camera.position, change)]
        camera.position = position
    except:
        receiver.socket.close()
