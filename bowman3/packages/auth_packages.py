from .core import Package

class HanshakePackage(Package):
    PACKAGE_ID = 0x00

    def _dump(self, socket):
        socket.send(b"\x00\x00")
    
    @classmethod
    def load(cls, socket):
        d = socket.recv(2)
        return cls()

    def handle(self, player):
        print("YAHOOO!")

