# Natas 32

#### URL: http://natas32.natas.labs.overthewire.org/
#### Credenciales: natas32:NaIWhW2VIrKqrc7aroJVHOZvk3RQMi0B

Aunque en el [nivel anterior](https://github.com/Calana2/Writeups_es/blob/main/OverTheWire-Wargames/Natas/natas31.md) explotamos una vulnerabilidad de AFR, no mencionamos que esta era escalable a RCE

La funcion open() abre un descriptor de archivo a una ruta de archivo `a menos que un caracter "|" sea agregado al final de la cadena`. En ese caso open() `ejecutará el archivo`

![2025-03-21-153857_1366x768_scrot](https://github.com/user-attachments/assets/00f08b5f-5569-4959-bc4c-8bb481599e84)








