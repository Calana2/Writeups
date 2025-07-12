## ASLR en Linux
Se aplica segun el contenido de `/proc/sys/kernel/randomize_va_space`. El ASLR en Linux no se puee forzar por binario.

| Valor | Significado |
| ----- | ----------- |
| 0 |	ASLR desactivado	Nada se aleatoriza |
| 1	| Parcial	Stack, mmap, VDSO, bibliotecas compartidas |
| 2	| Completo (por defecto)	Todo lo anterior + heap y segmentos de datos (brk()) |

## ASLR en Windows
Se puede desactivar de manera global con:
```ps1
Set-ProcessMitigation -System -Disable ASLR
```
Pero algunos binarios pueden seguir usando ASLR si fueron compilados con relocaciones y DYNAMICBASE

## PIE, DEP y Stack Cookies en GCC

| Flag | Significado |
| ----- | ----------- |
| -fno-pie -no-pie | Evita que el binario se cargue en direcciones aleatorias
| -z execstack	| Permite ejecutar código en la pila (stack ejecutable) |
| -fno-stack-protector | Desactiva los canarios que detectan desbordamientos |

## ASLR, DEP y Stack Cookies en MinGW
- **En MinGW, los binarios no son PIE por defecto**
- **En Windows, el formato PE permite que el sistema reubique el binario incluso si no fue compilado como PIE, gracias a la tabla de relocaciones que se incluye por defecto**

| Flag | Significado |
| ----- | ----------- |
| -Wl,--dynamicbase:no | Desactiva ASLR para el binario |
| -Wl,--nxcompat:no | Permite que la pila sea ejecutable |
| -fno-stack-protector | Desactiva los canarios que detectan desbordamientos |

## Compilar como codigo de 32bits/i386 en sistemas de 64 bits
| Compilador | Flag |
| ---------- | ---- |
| gcc | -m32 |


