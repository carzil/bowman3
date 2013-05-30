from .core import Package
from ..loggers import worker_log

class UsernamePackage(Package):
    PACKAGE_ID = 0x00

    def __init__(self, name):
        self.username = name

    def _dump(self, stream):
        stream.write_utf8(self.username)
    
    @classmethod
    def load(cls, stream):
        name = stream.read_utf8()
        return cls(name)

    def handle(self, player):
        player.username = self.username
        worker_log.info("%s was authenticated", self.username)

