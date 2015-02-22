import bge

from receivers import Receiver


receiver = Receiver(9002)
previousX = previousZ = 0


def camera(controller):
    global previousX, previousZ
    packet = 1
    while packet is not None:
        try:
            packet = next(receiver)
        except BlockingIOError:
            packet = None
        except:
            print("CLOSING")
            close()
            raise
        if not packet:
            previousX = 0
            previousZ = 0
            continue
        currX = packet.lhpp[0]
        changeX = (currX - previousX)
        changeX = change if abs(change) > 0.2 and 0 not in (currX, previousX) else 0
        previousX = currX
        controller.actuators["Motion"].torque = [0, 0, changeX]
        controller.activate(controller.actuators["Motion"])
        

def close(controller):
    print("QUITTING CLOSING")
    receiver.socket.close()
    import bge
    bge.logic.getCurrentScene().end()