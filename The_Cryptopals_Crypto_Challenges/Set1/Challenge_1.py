import base64
hex = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
raw = bytes.fromhex(hex)
base64Text = base64.b64encode(raw).decode()
print(base64Text)
