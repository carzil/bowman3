from bowman3.server.packages.auth_packages import HanshakePackage
import socket

p = HanshakePackage()
s = socket.socket()
s.connect(("localhost", 9889))
p.dump(s)
s.close()