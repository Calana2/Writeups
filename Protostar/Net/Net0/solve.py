import socket
import struct

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("0.0.0.0",2999))

n = s.recv(1024)
print(n)
n = n.split(b"'")[1].split(b"'")[0]

n = struct.pack("I",int(n))
s.send(n)

print(s.recv(1024))
