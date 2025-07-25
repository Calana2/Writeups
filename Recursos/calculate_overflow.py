#!/bin/python3
from pwn import *

p = process("./process")

# Once you find the 4-byte pattern at ESP/RSP
# offset = cyclic_find("kaaa")

raw_input("attach gdb")
p.sendline(cyclic(500))
p.interactive()

# There are more elegant ways
