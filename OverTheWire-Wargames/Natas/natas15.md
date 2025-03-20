# Natas 15

#### URL: http://natas15.natas.labs.overthewire.org
#### Credenciales: natas15:SdqIqBsFcz3yotlNYErZSZwblkm0lrvx

Aqui necesitamos obtener la contraseña por medio de una inyección SQL, pero el programa solo nos dice que el usuario existe si el resultado de la peticion devuelve al menos una fila

``` php
if(mysqli_num_rows($res) > 0) {
        echo "This user exists.<br>";
    } else {
        echo "This user doesn't exist.<br>";
```

Tendremos que hacerlo a ciegas, probando caracter a caracter hasta encontrar los 32 caracteres validos de la contraseña. Haré eso en python y usando varios hilos para ser más rápido:

