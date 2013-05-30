from bowman3.packages.auth_packages import UsernamePackage
from bowman3.utils.stream import Stream
import socket

s = socket.socket()
s.connect(("localhost", 9889))
st = Stream(s)
p = UsernamePackage(input("Your username: "))
p.dump(st)
s.close()
