from Crypto.Cipher import AES
import base64

"""
def AES_CBC_Decrypt(key, iv, data):
    cipher = AES.new(key, AES.MODE_CBC)
    cipher.IV = iv
    plaintext = cipher.decrypt(data)
    return plaintext
"""

def fixed_xor(var1, var2):
    if len(var1) != len(var2):
        print("Params must be the same length")
        return bytes(0)
    result = []
    for i in range(0, len(var1)):
        result.append(var1[i] ^ var2[i])
    return bytes(result)

def AES_ECB_Decrypt(key, data):
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.decrypt(data)
    return plaintext

def AES_CBC_Decrypt(key,iv,raw_data):
    # manual approach
    plaintext = b""
    previous_block = iv
    block_size = AES.block_size
    for i in range(0,len(raw_data),block_size):
        current_block = raw_data[i:i+block_size]
        decrypted = AES_ECB_Decrypt(key,current_block)
        plaintext_block = fixed_xor(decrypted,previous_block)
        plaintext += plaintext_block
        previous_block = current_block
    return plaintext


try:
    with open('10.txt') as file:
        data = file.read()
        raw_data = base64.b64decode(data)
        key = b"YELLOW SUBMARINE"
        iv = b"0" * 16
        plaintext = AES_CBC_Decrypt(key,iv,raw_data)
        print(plaintext.decode(errors="ignore"))
except FileNotFoundError:
    print("File not found")

