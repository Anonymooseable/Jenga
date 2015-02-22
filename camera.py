import bge

from receivers import Receiver

def close(controller):
    print("QUITTING CLOSING")
    try:
        receiver.socket.close()
    except:
        pass
    bge.logic.getCurrentScene().end()

try:
    receiver = Receiver(9002)
except:
    close()
    raise
previousX = previousZ = 0
currScale = 1

def clamp(x, lower, upper):
    return max(min(x, upper), lower)

def camera(controller):
    global previousX, previousZ, currScale
    packet = 1
    while packet is not None:
        try:
            packet = next(receiver)
        except BlockingIOError:
            packet = None
        except:
            close()
            raise
        if not packet:
            previousX = previousZ = 0
            continue
        currX = packet.lhpp[0]
        changeX = (currX - previousX) if 0 not in (currX, previousX) else 0
        previousX = currX

        currZ = packet.lhpp[2]
        changeZ = (currZ - previousZ)/100 if 0 not in (currZ, previousZ) else 0
        previousZ = currZ
        currScale *= 2**changeZ
        currScale = clamp(currScale, 0.6, 4)
        controller.owner.worldScale = [currScale]*3

        controller.actuators["Motion"].torque = [0, 0, changeX]
        controller.activate(controller.actuators["Motion"])
