from pwn import *
import os

args = ["A"]*99
args[64]="\x00"
args[65]="\x20\x0a\x0d"
args[66]="4444"

r,w = os.pipe()
with open("\x0a","wb") as f:
        f.write(b"\x00\x00\x00\x00")
io = process(["/home/input2/input2"]+args,
            stderr=r,
            env={"\xde\xad\xbe\xef":"\xca\xfe\xba\xbe"},
            )
io.sendline(b"\x00\x0a\x00\xff")
os.write(w,b"\x00\x0a\x02\xff")

conn = remote("localhost",4444)
conn.sendline(b"\xde\xad\xbe\xef")

io.interactive()
