# Natas 28

#### URL: http://natas28.natas.labs.overthewire.org
#### Credenciales: natas28:1JNwQM1Oi6J6j1k49Xyw7ZN6pXMQInVj

Cuando introducimos cualquier cosa vemos que la peticion POST se tranforma en un GET con un parametro "query" cifrado:

![2025-03-21-114416_822x355_scrot](https://github.com/user-attachments/assets/8974c9ed-e481-4fd2-afca-b8a36cd11234)

![2025-03-21-114450_955x52_scrot](https://github.com/user-attachments/assets/38ff6e4e-0d21-49ba-93e5-d850d70ed542)

![2025-03-21-115134_1366x476_scrot](https://github.com/user-attachments/assets/cf796ae4-d30f-43e7-82e2-19d0f2fe6a5d)

Usan PKCS#7 para el padding:

![2025-03-21-115352_891x300_scrot](https://github.com/user-attachments/assets/0fdc3fe8-1b3e-4ad1-b87f-273768203031)


Creamos un pequeño script para realizar peticiones y observar la query:
``` python
import requests
from base64 import b64encode


URL='http://natas28.natas.labs.overthewire.org'
headers={'Authorization':f'Basic {b64encode(b"natas28:1JNwQM1Oi6J6j1k49Xyw7ZN6pXMQInVj").decode()}'}

for i in range(1,34):
    data={'query':'A'*i}
    x = requests.post(URL,headers=headers,data=data)
    print(f"QUERY: {x.url.split("=")[1]}")
```

``` bash
 python3 test.py
QUERY: G%2BglEae6W%2F1XjA7vRm21nNyEco%2Fc%2BJ2TdR0Qp8dcjPKjd8MKDZZIiKG51FNeoPjUvfoQVOxoUVz5bypVRFkZR5BPSyq%2FLC12hqpypTFRyXA%3D
QUERY: G%2BglEae6W%2F1XjA7vRm21nNyEco%2Fc%2BJ2TdR0Qp8dcjPKYsNYgsg1hFJebd%2BJNix06SHmaB7HSm1mCAVyTVcLgDq3tm9uspqc7cbNaAQ0sTFc%3D
QUERY: G%2BglEae6W%2F1XjA7vRm21nNyEco%2Fc%2BJ2TdR0Qp8dcjPJ8EmoxKU1njKubmw7%2BRDt1mi4rXbbzHxmhT3Vnjq2qkEJJuT5N6gkJR5mVucRLNRo%3D
QUERY: G%2BglEae6W%2F1XjA7vRm21nNyEco%2Fc%2BJ2TdR0Qp8dcjPK02918sQNUadassvlSAHDHKSh%2FPMVHnhLmbzHIY7GAR1bVcy3Ix3D2Q5cVi8F6bmY%3D
QUERY: G%2BglEae6W%2F1XjA7vRm21nNyEco%2Fc%2BJ2TdR0Qp8dcjPJLk0xdEarIh%2BMvTkV61TlvrDuHHBxEg4a0XNNtno9y9GVRSbu6ISPYnZVBfqJ%2FOns%3D
QUERY: G%2BglEae6W%2F1XjA7vRm21nNyEco%2Fc%2BJ2TdR0Qp8dcjPJ%2BDZedSJQqwrZX9tfUGM7WQcCYxLrNxe2TV1ZOUQXdfmTQ3MhoJTaSrfy9N5bRv4o%3D
QUERY: G%2BglEae6W%2F1XjA7vRm21nNyEco%2Fc%2BJ2TdR0Qp8dcjPKvwmKMYUAmbbaAruK1epuIZIaVSupG%2B5Ppq4WEW09L0Nf%2FK3JUU%2FwpRwHlH118D44%3D
QUERY: G%2BglEae6W%2F1XjA7vRm21nNyEco%2Fc%2BJ2TdR0Qp8dcjPLNQ6RxZsY7UPRe5yiycfUiiW3pCIT4YQixZ%2Fi0rqXXY5FyMgUUg%2BaORY%2FQZhZ7MKM%3D
QUERY: G%2BglEae6W%2F1XjA7vRm21nNyEco%2Fc%2BJ2TdR0Qp8dcjPKIFsYeK8Y3JmD4ecRfI3d%2BoJUi8wHPnTascCPxZZSMWpc5zZBSL6eob5V3O1b5%2BMA%3D
```

Podemos ver que se repite un patron, asumimos que la query esta compuesta por PREFIJO + DATA + SUFIJO + PADDING y que presumiblemente estan usando AES-ECB porque es en el modo de operacion ECB en el que bloques iguales obtienen el mismo cifrado para la misma clave.

Hacemos un script para encontrar el tamaño de bloque del cifrado:
``` python
import requests
from base64 import b64encode, b64decode
from urllib.parse import unquote


URL='http://natas28.natas.labs.overthewire.org'
headers={'Authorization':f'Basic {b64encode(b"natas28:1JNwQM1Oi6J6j1k49Xyw7ZN6pXMQInVj").decode()}'}

for i in range(1,50):
    data={'query':'A'*i}
    x=requests.post(URL,headers=headers,data=data)
    encryptedData=x.url.split("?")[1].split("=")[1]
    rawData = b64decode(unquote(encryptedData))
    print(f"Encrypted data Length:[{len(rawData)}] Query Length:[{len(data['query'])}]")
```

```
python3 test.py
Encrypted data Length:[80] Query Length:[1]
Encrypted data Length:[80] Query Length:[2]
Encrypted data Length:[80] Query Length:[3]
Encrypted data Length:[80] Query Length:[4]
Encrypted data Length:[80] Query Length:[5]
Encrypted data Length:[80] Query Length:[6]
Encrypted data Length:[80] Query Length:[7]
Encrypted data Length:[80] Query Length:[8]
Encrypted data Length:[80] Query Length:[9]
Encrypted data Length:[80] Query Length:[10]
Encrypted data Length:[80] Query Length:[11]
Encrypted data Length:[80] Query Length:[12]
Encrypted data Length:[96] Query Length:[13]
Encrypted data Length:[96] Query Length:[14]
Encrypted data Length:[96] Query Length:[15]
Encrypted data Length:[96] Query Length:[16]
Encrypted data Length:[96] Query Length:[17]
Encrypted data Length:[96] Query Length:[18]
Encrypted data Length:[96] Query Length:[19]
Encrypted data Length:[96] Query Length:[20]
Encrypted data Length:[96] Query Length:[21]
Encrypted data Length:[96] Query Length:[22]
Encrypted data Length:[96] Query Length:[23]
Encrypted data Length:[96] Query Length:[24]
Encrypted data Length:[96] Query Length:[25]
Encrypted data Length:[96] Query Length:[26]
Encrypted data Length:[96] Query Length:[27]
Encrypted data Length:[96] Query Length:[28]
Encrypted data Length:[112] Query Length:[29]
Encrypted data Length:[112] Query Length:[30]
```

Como se observa el tamaño de bloque es 16, porque al pasar de 12 a 13 y de 28 a 29 los datos encriptados aumentan en 16 bytes. El prefijo parece ser de 32 bytes o 2 bloques.



``` bash
python3 natas28_sploit.py
<html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src=http://natas.labs.overthewire.org/js/wechall-data.js></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas28", "pass": "1JNwQM1Oi6J6j1k49Xyw7ZN6pXMQInVj" };</script></head>
<body>
<!-- morla/10111 -->
<h1>natas28</h1>
<style>
ul {
  margin: 1em 0;
  padding: 0 0 0 40px;
}

li {
  margin: 1em 0;
}
</style>
<div id="content">
<h2> Whack Computer Joke Database</h2><ul><li>31F4j3Qi2PnuhIZQokxXk1L3QT9Cppns</li></ul>
</div>
</body>
</html>

http://natas28.natas.labs.overthewire.org/search.php/?query=G%2BglEae6W/1XjA7vRm21nNyEco/c%2BJ2TdR0Qp8dcjPLAhy3ui8kLEVaROwiiI6OeWnPci/qKte0ohRTkObF%2BT5ujPcGtKfnu/mSL/syLoz1W9Y2gUEVDr09KHPcw89z2vfoQVOxoUVz5bypVRFkZR5BPSyq/LC12hqpypTFRyXA%3D
```
