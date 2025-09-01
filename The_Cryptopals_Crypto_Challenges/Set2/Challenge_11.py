from Crypto.Cipher import AES
from random import randint

def xor(var1, var2):
    result = []
    for i in range(0, len(var1)):
        result.append(var1[i] ^ var2[i])
    return bytes(result)

def pkcs7_pad(chunk: bytes, block_size: int):
    plen = block_size - (len(chunk) % block_size)
    pad = bytes([plen] * plen)
    return chunk + pad

def AES_ECB_Encrypt(key, data):
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.encrypt(data)
    return plaintext

def AES_CBC_Encrypt(iv, key, data):
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    plaintext = cipher.encrypt(data)
    return plaintext

def Padding_Oracle(input):
    global mode
    ciphertext = bytearray()
    try:
        with open("/dev/urandom","rb") as f:
            key = f.read(16)
            bpad = f.read(randint(5,10))
            apad = f.read(randint(5,10))
            plaintext = pkcs7_pad(bpad + input + apad,16)
            if randint(0,1):
                ciphertext = AES_ECB_Encrypt(key,plaintext)
                mode = "ECB"
            else:
                iv = f.read(16)
                ciphertext = AES_CBC_Encrypt(iv,key,plaintext)
                mode = "CBC"
    except FileNotFoundError:
            print("File not found, are you using Windows?")
    return ciphertext

def Detect_AES_ECB_Mode(data, key_size: int = 16):
    blocks = set()
    for i in range(0, len(data), key_size):
        block = data[i:i + key_size]
        if block in blocks:
            return True
        blocks.add(block)
    return False

mode = ""
hits = 0
num_probes = 1000
for i in range(num_probes):
    message = Padding_Oracle(b"A"*43)
    isECB = Detect_AES_ECB_Mode(message)
    if (isECB and mode == "ECB") or (not isECB and mode == "CBC"):
        hits+=1
print("[!] Executing Detection Oracle...")
print(f"Efectiveness: {hits / num_probes * 100:.2f}%")

