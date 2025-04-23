def repeated_xor(msg, key):
    if len(key) > len(msg):
        print("Key must be less or equal than the message")
    result = []
    key_index = 0
    for i in range(0,len(msg)):
        result.append(msg[i] ^ key[key_index])
        key_index = (key_index+1) % len(key)
    return bytes(result)

msg = b"Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
key = b"ICE"

result = repeated_xor(msg,key)
print(result.hex())
