raw = bytes.fromhex("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")

for k in range(256):
    buffer = bytearray()
    for byte in raw:
        buffer.append(byte ^ k)
    is_printable = all(32 <= b <= 126 for b in buffer)
    if is_printable:
        print(f"Key={chr(k)}: {buffer.decode('ascii')}")
