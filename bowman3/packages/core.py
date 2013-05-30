import struct

class Package:
    def dump(self, socket):
        socket.send(struct.pack(">H", self.PACKAGE_ID))
        if hasattr(self, "_dump"):
            self._dump(socket)
