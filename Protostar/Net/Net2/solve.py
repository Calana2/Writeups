import socket
import struct

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("0.0.0.0",2998))

sum = 0
for i in range(4):
    n = s.recv(4)
    sum += struct.unpack("I",n)[0]
print(sum)

# Empaquetamos la suma antes de enviarla
s.send(struct.pack("I",sum))
print(s.recv(1024))
