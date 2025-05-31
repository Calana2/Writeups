# badchars

**Nota importante**: Sufri durante un buen rato tratando de descubrir porque el exploit no funcionaba especificamente en un byte de '.data'. Resulta ser que .data+7 contenia 0x2e o '.' (un badchar) en esa direccion, entonces no se puede escribir ahi porque el sanitizador lo reemplaza por \xeb. Por esta razon escribi en `.bss`, que tenia 8 bytes, rezando que el byte despues de este fuera un null byte.

## x86

## x86_64
