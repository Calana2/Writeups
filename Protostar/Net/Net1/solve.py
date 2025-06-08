import socket
import struct

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("0.0.0.0",2997))

n = s.recv(4)
print(n)

n = struct.unpack("I",n)[0]
s.send(str(n).encode())
print(s.recv(1024))
