def XORBruteForceLine(line, linenum):
    raw = bytes.fromhex(line)
    output = []
    for k in range(256):
        buffer = bytearray()
        for byte in raw:
            buffer.append(byte ^ k)
        is_printable = all(32 <= b <= 126 or b in {9,10} for b in buffer)
        if is_printable:
            output.append(f"Key={chr(k)} --- Text={buffer.decode('ascii')}")
    if len(output) == 0:
        return
    print(f"\n======== LINE {linenum} ========\n")
    for l in output:
        print(l)
try:
    with open("4.txt", "r") as f:
        for n,l in enumerate(f.readlines()):
            XORBruteForceLine(l,n)
except FileNotFoundError:
    print("Error: File not found.")
