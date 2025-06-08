# Net Zero

``` C
#include "../common/common.c"

#define NAME "net0"
#define UID 999
#define GID 999
#define PORT 2999

void run()
{
  unsigned int i;
  unsigned int wanted;

  wanted = random();

  printf("Please send '%d' as a little endian 32bit int\n", wanted);

  if(fread(&i, sizeof(i), 1, stdin) == NULL) {
      errx(1, ":(\n");
  }

  if(i == wanted) {
      printf("Thank you sir/madam\n");
  } else {
      printf("I'm sorry, you sent %d instead\n", i);
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

Segun el codigo fuente, el programa nos envia un entero y debemos devolverselo en formato bytes en little endian.

El programa esta en escucha en el puerto 2999.

Para convertir entero de 4 bytes a little-endian se puede usar el modulo `struct`:
``` python
import socket
import struct

# Crear un socket para conectarnos al puerto 2999
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("0.0.0.0",2999))

# Recibir los datos y extraer el numero
n = s.recv(1024)
print(n)
n = n.split(b"'")[1].split(b"'")[0]

# Enviar en little-endian bytes
n = struct.pack("I",int(n))
s.send(n)

print(s.recv(1024))
```




