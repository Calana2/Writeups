# x86 101: Introduccion General

#### Creditos de las imagenes a `flipthebit`

## Arquitectura x86

#### Formato de almacenamiento
Little Endian: El byte menos significativo (LSB) se almacena en la direccion de memoria mas baja.
#### Registros de la CPU
En la arquitectura x86 tenemos 8 registros de proposito general, 6 registros de segmento, 1 registro de banderas y 1 puntero de instruccion.

Algunos registros de proposito general son mas especificos:
EAX: Usado en operaciones aritmeticas
EBX: Usado como puntero a los datos
ECX: Usado en bucles e instrucciones de desplazamiento y rotacion
EDX: Usado en operaciones aritmeticas y de entrada/salida
ESP: Apunta a la cima de la pila
EBP: Apunta a la base de la pila
ESI: Apunta al origen en operaciones de flujo
EDI: Apunta al destion en operaciones de flujo

Los registros de proposito general son de 32 bits o 4 bytes, tienen subregistros de 16 bytes (parte baja) y estos a su vez tienen subregistros de 8 bytes (parte baja), ejemplo: EAX -> AX -> AL. Los prefijos son intuitivos, `E`xtended, `L`ower.

EFLAGS: Registro de bandera para soporte de funciones aritmeticas y depuracion.

EIP: Puntero de instruccion, apunta a la siguiente instruccion a ejecutarse

#### Palabras que refieren a tamaños de valores
- `byte`, entero de 8 bits
- `word`, entero de dos bytes
- `dword`, entero de 4 bytes
- `quadword`, entero de 8 bytes

#### Estructura de memoria de un program ELF en x86
- Memoria reservada para capturar errores de punteros nulos: `0x00000000 00000000` - **`0x00000000 00400000`**
- Text: Codigo ejecutable
- Data: Variables globales y estaticas inicializadas
- BSS: Variables globales/estaticas no inicializadas
- Heap (monton): Memoria dinamica, crece hacia direcciones altas
- Mapeo de memoria: Librerias compartida
- Stack (pila): Crece hacia direcciones bajas
- Espacio del Kernel: `0xffff800000000000` y superiores, solo accesible para el kernel
  
![2025-04-04-144222_358x551_scrot](https://github.com/user-attachments/assets/a8052180-98da-4a85-b537-21af04c6c3ae)

#### Memoria 

 Las direcciones de memoria son de 32 bits o 4 bytes, permitiendo asignar 2^32 bits = 4.29497e+09 / 1024 / 1024 = 4 gb de memoria.

 Cada programa cree que tiene acceso a toda la memoria del sistema, desde 0x00000000 hasta 0xffffffff, a esto se le llama `memoria virtual` o `espacio de direcciones virtual`, el sistema operativo controla esto mediante `tablas de paginas` que traduce direcciones virtuales en fisicas.

### Marco de pila y convencion de llamadas

La pila se compone de stack frames o `marcos de pila`, uno para cada procedimiento o funcion:

![2025-04-04-144236_911x545_scrot](https://github.com/user-attachments/assets/132960bf-f011-4282-b302-a6cc859786c1)

En la arquitectura x86 la estructura de un stack frame es la siguiente (de la direccion mas alta a la mas baja):
- Variables locales de la funcion
- EBP almacenado (usado para volver a frames anteriores, apuntando ESP al ultimo EBP antes de salir de la funcion)
- Direccion de retorno
- Parametros de la funcion

![2025-04-04-144247_704x539_scrot](https://github.com/user-attachments/assets/f972aef2-bf72-44fd-98c8-23974f660750)

Se le llama `caller` a la funcion invocadora y `callee` a la funcion invocada.

En Linux el `caller` se encarga tanto de reservar espacio en el stack como limpiar la pila una vez termine el `callee` (convencion `cdecl`)

En Windows el `callee` limpia la pila (convencion `stdcall`)


### Alineacion de la pila

El sistema necesita que los datos estén organizados en direcciones de memoria que cumplan con ciertos múltiplos, en este caso 4 bytes al llamar funciones.


## Arquitectura x86_64

#### Registros de la CPU

En la arquitectura x86_64 tenemos 16 registros de proposito general, 6 registros de segmento, 1 registro de banderas y 1 puntero de instruccion.

Los registros EAX,EBX,ECX,EDX,ESP,EBP,ESI,EDI  asi como el resto de registros fueron extendidos a 64 bits de almacenamiento, y su version completa cuenta con una R al inicio del nombre, por ejemplo: EAX (32 bits) --> RAX (64 bits) mientras EAX sigue siendo accesible como parte baja de EAX.

Se añaden los registros r8,r9,r10,r11,r12,r13,r14,r15 de 64 bits con sus respectivas partes bajas de 32 bits (r8d), parte baja de 16 bits (r8w) y parte baja de 8 bits (r8b). Los prefijos hacen referencia al tamaño de los valores, `d`ouble, `w`ord y `b`yte.

### Memoria

 Las direcciones de memoria son de 64 bits u 8 bytes, permitiendo asignar 2^64 bits = 256 TB teoricamente. Normalmente se usan direcciones de memoria de 48 bits porque es suficiente.
 
### Marco de pila y convencion de llamadas

Los parametros del procedimento son pasados en dependencia de la ABI(Application Binary Interface) en uso. 

GNU/Linux usa System V AMD64 ABI, o sea, los 6 primeros parametros de funcion se pasan mediante rdi, rsi, rdx, rcx, r8, y r9, y el resto mediante el stack. El caller sigue encargandose de la limpieza de la pila igual.

Windows usa su propia ABI x64 donde los 4 primeros parametros de funcion se pasan mediante los registros rcx, rdx, r8 y r9, y el resto mediante el stack. Entre llamadas a función existen los registros volatiles (los que cambian durante la llamada) y los no volatiles (el destinatario de la llamada debe conservarlo). La API de Windows usa la nueva convencion `fastcall`, donde el callee limpia igual pero ahora se exige al caller a reservar un espacio fijo de 32 bytes llamado "shadow space".

Aunque ahora se puede usar RSP con desplazamiento y prescindir de EBP, este se sigue usando porque hace mas sencilla la depuracion.


### Alineacion de la pila

La pila debe estar alineada a 16 bytes antes de una llamada a funcion porque instrucciones extendidas requieren datos alineados a 16/32 bytes y esto mejora el rendimiento en los accesos a memoria.

El caller debe alinear el stack antes de la llamada. Se debe cumplir que: `(RSP - 8) % 16 == 0`
