# Implementing PKCS#7 padding

![2025-06-15-191411_1007x367_scrot](https://github.com/user-attachments/assets/97eae380-8689-4a94-bacb-4a68b86d59a5)

Es bastante sencillo. Consiste en que al ultimo bloque del mensaje a cifrar se le añade un padding de N bytes, donde cada byte vale igualmente N.

Para evitar ambiguedades si el ultimo bloque es multiplo del tamaño de bloque se añade un bloque entero de padding.

