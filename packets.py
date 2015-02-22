from collections import namedtuple
import struct


BasePacket = namedtuple('Packet', ['lhpp', 'rhpp', 'rtf', 'rif'])


class Packet(BasePacket):
    structure = 'd' * 12

    @classmethod
    def reset(cls):
        return cls(*[(0, 0, 0)]*4)

    def pack(self):
        fields = (axis for vector in self for axis in vector)
        return struct.pack(self.structure, *fields)

    @classmethod
    def unpack(cls, packet):
        fields = struct.unpack(cls.structure, packet)
        fields = [fields[i:i+3] for i in range(0, len(fields), 3)]
        return cls._make(fields)
