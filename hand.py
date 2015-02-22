from receivers import Receiver


receiver = Receiver(9001)


def hand(controller):
    print(dir(controller))
    for vector in iter(receiver):
        print(vector)


if __name__ == '__main__':
    hand(1)
