def detectAESInECBMode(data: bytes, keysize: int) -> bool:
    blocks = set()
    for i in range(0,len(data),16):
        block = data[i:i+keysize]
        if block in blocks:
            return True
        blocks.add(block)
    return False

def detectECBFile(lines: list[str]):
    for i,line in enumerate(lines):
        data = bytes.fromhex(line)
        if detectAESInECBMode(data,16):
            return i+1,line
    return 0,""

try:
    with open('8.txt') as file:
        lines = file.readlines()
        linenum, line = detectECBFile(lines)
        if line != "":
         print("Block whit AES-ECB found:")
         print(f"{linenum}: {line}") 

except Exception as e:
    print(f"Error {e}")

