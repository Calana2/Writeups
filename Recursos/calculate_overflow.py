#!/bin/python3
from pwn import *
# set terminal gdb will run in
# replace 'tmux' with your terminal
context.terminal = ['tmux', 'splitw', '-hp', '70']

# create payload
payload = cyclic(60, n=4)

# debug rop chain
io = gdb.debug('./filename', '''
               b func
               c
               ''')
# `continue` to see the crash
# `cyclic -l 0xvalue_at_the_top_of_the_stack -n 4`
io.sendline(payload)

# keep the program alive
io.interactive()
