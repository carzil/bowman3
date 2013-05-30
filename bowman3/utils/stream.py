import struct

INT_FORMAT = ">I"
SHORT_FORMAT = ">H"

INT_LEN = struct.calcsize(INT_FORMAT)
SHORT_LEN = struct.calcsize(SHORT_FORMAT)

class Stream:
    def __init__(self, socket):
        self._socket = socket

    def write_int(self, int_):
        return self._socket.send(struct.pack(INT_FORMAT, int_))

    def write_short(self, short_):
        return self._socket.send(struct.pack(SHORT_FORMAT, short_))

    def write_bytes(self, bytes_):
        self.write_int(len(bytes_))
        return self._socket.send(bytes_)

    def write_utf8(self, str_):
        self.write_bytes(str_.encode("utf-8"))

    def read_short(self):
        s = self._socket.recv(INT_LEN)
        return struct.unpack(INT_FORMAT, s)[0]

    def read_int(self):
        s = self._socket.recv(INT_LEN)
        return struct.unpack(INT_FORMAT, s)[0]

    def read_bytes(self):
        l = self.read_int()
        return self._socket.recv(l)

    def read_utf8(self):
        k = self.read_bytes()
        return k.decode("utf-8")
