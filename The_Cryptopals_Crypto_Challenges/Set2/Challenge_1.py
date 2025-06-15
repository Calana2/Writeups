def pkcs7_pad(chunk: bytes, block_size: int):
    if len(chunk) > block_size:
        return b""
    plen = block_size - (len(chunk) % block_size)
    pad = bytes([plen] * plen)
    return chunk + pad

def pkcs7_unpad(pchunk: bytes):
    plen = pchunk[-1]
    if pchunk[-plen:] != bytes([plen] * plen):
        raise ValueError("Padding invalido.")
    return pchunk[:-plen]

padded = pkcs7_pad(b"YELLOW SUBMARINE",20)
unpadded = pkcs7_unpad(padded)

print(padded)
print(unpadded)
