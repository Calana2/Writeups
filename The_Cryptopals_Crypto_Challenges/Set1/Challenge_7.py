from Crypto.Cipher import AES
import base64

def AES_ECB_Decrypt(key, data):
    cipher = AES.new(key,AES.MODE_ECB)
    plaintext = cipher.decrypt(data)
    return plaintext


try:
    with open('7.txt','r') as file:
        data = file.read()
        raw_data = base64.b64decode(data)
        key = b"YELLOW SUBMARINE"
        plaintext = AES_ECB_Decrypt(key,raw_data)
        print(plaintext.decode())

except FileNotFoundError:
    print("File not found")
