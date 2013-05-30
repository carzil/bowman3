import struct

class Package:
    def dump(self, stream):
        stream.write_short(self.PACKAGE_ID)
        if hasattr(self, "_dump"):
            self._dump(stream)
