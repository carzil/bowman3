class Player:
    def __init__(self, sock, addr):
        self.socket = sock
        self.host, self.port = addr
