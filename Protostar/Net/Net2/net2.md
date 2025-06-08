# Net Two

```
#include "../common/common.c"

#define NAME "net2"
#define UID 997
#define GID 997
#define PORT 2997

void run()
{
  unsigned int quad[4];
  int i;
  unsigned int result, wanted;

  result = 0;
  for(i = 0; i < 4; i++) {
      quad[i] = random();
      result += quad[i];

      if(write(0, &(quad[i]), sizeof(result)) != sizeof(result)) {
          errx(1, ":(\n");
      }
  }

  if(read(0, &wanted, sizeof(result)) != sizeof(result)) {
      errx(1, ":<\n");
  }


  if(result == wanted) {
      printf("you added them correctly\n");
  } else {
      printf("sorry, try again. invalid\n");
  }
}

int main(int argc, char **argv, char **envp)
{
  int fd;
  char *username;

  /* Run the process as a daemon */
  background_process(NAME, UID, GID); 
  
  /* Wait for socket activity and return */
  fd = serve_forever(PORT);

  /* Set the client socket to STDIN, STDOUT, and STDERR */
  set_io(fd);

  /* Don't do this :> */
  srandom(time(NULL));

  run();
}
```

En este nos envia cuatro enteros en formato little-endian y debemos enviar de vuelta su suma:
``` python
import socket
import struct

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("0.0.0.0",2998))

sum = 0
for i in range(4):
    n = s.recv(4)
    sum += struct.unpack("I",n)[0]
print(sum)

# Empaquetamos la suma antes de enviarla
s.send(struct.pack("I",sum))
print(s.recv(1024))
```

## Tipos de datos, funciones de entrada y endianness

En el primer y ultimo reto se usa `read` para aceptar entrada de usuario, y la comparacion es `numerica`. Puesto que `read` lee bytes crudos y los almacena en un `unsigned int` debemos pasarlo en formato de bytes (little-endian porque es la disposicion de bytes que usa la arquitectura x86).

En el segundo reto se usa `fgets` que acepta una string o un array de chars como entrada.
