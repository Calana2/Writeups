# Natas 11

#### URL: http://natas11.natas.labs.overthewire.org/

#### Credenciales: natas11:UJdqkK1pTu6VLt9UHWAgRZz6sVUZ3lEk

Como la operacion XOR es reversible entonces si ciphertext = json_text ^ key, luego ciphertext ^ json_text = key. Presentamos esto en un script de python.

``` python
import requests
from urllib.parse import unquote
from base64 import b64encode, b64decode
from itertools import cycle

def xorEncrypt(op1,op2):
    
    return bytes(a ^ b for a, b in zip(op1,cycle(op2)))

URL="http://natas11.natas.labs.overthewire.org"
headers={'Authorization':f'Basic {b64encode(b"natas11:UJdqkK1pTu6VLt9UHWAgRZz6sVUZ3lEk").decode()}'}

x = requests.get(URL,headers=headers)
raw_cookie = b64decode(unquote(str(x.cookies.get('data'))))
json_data = b'{"showpassword":"no","bgcolor":"#ffffff"}'
print(xorEncrypt(raw_cookie,json_data))
```

``` bash
python3 natas11_sploit.py
b'eDWoeDWoeDWoeDWoeDWoeDWoeDWoeDWoeDWoeDWoe'
```

La clave es "edWoe". Ahora con la clave encriptamos nuestra cookie con "showpassword" cambiado y la codificamos en base64:




