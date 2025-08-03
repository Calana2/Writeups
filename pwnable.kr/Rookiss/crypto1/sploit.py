from pwn import *
import string

context.log_level = "error"

def get_ciphertext(id, pw=b""):
        #r = remote("pwnable.kr",9006)
        r = process(["nc","0","9006"])
        r.sendlineafter(b"ID\n",id)
        r.sendlineafter(b"PW\n",pw)
        l = r.recvline().strip().decode()
        r.close()
        c = l[l.find("(")+1:l.find(")")]
        return c

alphabet = string.digits + string.ascii_lowercase + "-_"
cookie=b""

for i in range(29):
    # Some math
    placeholder = b"-"*(13 - i + 16 * ((i+2)//16))
    test_placeholder = b"-"*(15 - i + 16 * ((i+2)//16))
    count = 32 * (i//16 + 1)
    # Get ciphertext
    cipher_1 = get_ciphertext(placeholder)
    # Guess one byte
    for c in alphabet:
        cipher_2 = get_ciphertext(test_placeholder + cookie + c.encode())
        if cipher_1[count-32:count] == cipher_2[count-32:count]:
              cookie += c.encode()
              print("Cookie updated!: ",cookie)
              break

# Win
id = b"admin"
pw = hashlib.sha256(id+cookie).hexdigest().encode()
print("Id: ",id)
print("Password: ",pw)
print("Cookie: ",cookie)

#r = process("pwnable.kr",9006)
r = process(["nc","0","9006"])
r.sendlineafter(b"ID\n",id)
r.sendlineafter(b"PW\n",pw)
r.interactive()
