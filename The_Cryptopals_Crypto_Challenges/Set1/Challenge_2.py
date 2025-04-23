def FixedXOR(s1: str , s2: str) -> str:
    raw_s1 = bytes.fromhex(s1)
    raw_s2 = bytes.fromhex(s2)
    assert(len(raw_s1) == len(raw_s2))
    s3 = bytes(raw_s1[i] ^ raw_s2[i] for i in range(len(raw_s1)))
    return s3.hex()

print(FixedXOR("1c0111001f010100061a024b53535009181c","686974207468652062756c6c277320657965"))
