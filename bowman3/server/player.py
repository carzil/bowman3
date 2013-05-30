from ..utils.stream import Stream

class Player:
    def __init__(self, sock, addr):
        self.stream = Stream(sock)
        self.host, self.port = addr
        self.username = None
