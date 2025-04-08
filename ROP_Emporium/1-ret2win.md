# ret2win

![2025-04-03-202444_1053x374_scrot](https://github.com/user-attachments/assets/dd203596-3a8c-4b37-9d8e-b17cdaf30a49)

## x86

Lo primero que hacemos es revisar las propiedades del ejecutable. Hay varias utilidades para hacer esto (`checksec`,`rabin2`,`readelf`,etc...)

```
checksec --file=ret2win
RELRO           STACK CANARY      NX            PIE             RPATH      RUNPATH	Symbols		FORTIFY	Fortified	Fortifiable	FILE
Partial RELRO   No canary found   NX enabled    No PIE          No RPATH   No RUNPATH   69 Symbols	  No	0		3		ret2win
```



