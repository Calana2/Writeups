import math
import base64
FILENAME = "6.txt"

# Frecuencias del inglés
english_frequencies = {
    'E': 12.02, 'T': 9.10, 'A': 8.12, 'O': 7.68, 'I': 7.31, 'N': 6.95,
    'S': 6.28, 'H': 6.09, 'R': 5.99, 'D': 4.32, 'L': 4.03, 'U': 2.88,
    'C': 2.71, 'M': 2.61, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'P': 1.82,
    'Y': 1.75, 'B': 1.49, 'V': 1.11, 'K': 0.69, 'X': 0.17, 'J': 0.10,
    'Q': 0.10, 'Z': 0.07, ' ': 13.00
}

# Calcular el puntaje del texto según frecuencias esperadas
def english_score(data):
    letter_counts = {}
    total_letters = 0
    for byte in data:
        char = chr(byte).upper()
        if 'A' <= char <= 'Z' or char == ' ':
            letter_counts[char] = letter_counts.get(char, 0) + 1
            total_letters += 1
    
    score = 0
    if total_letters > 0:
        for char, freq in english_frequencies.items():
            observed = letter_counts.get(char, 0)
            score += observed * freq  # Ponderación directa según frecuencia
            score -= abs(observed / total_letters - freq) / 10  # Penalización
    
    return score

# Calcular distancia de Hamming
def hamming_distance(bytes1, bytes2):
    if len(bytes1) != len(bytes2):
        raise ValueError("Arrays must have the same length")
    return sum(bin(b1 ^ b2).count('1') for b1, b2 in zip(bytes1, bytes2))

# Leer archivo y calcular distancia de Hamming normalizada
def normalized_hamming_distance(data, blocksize):
    n_blocks = len(data) // (blocksize * 2)
    hd_normalized = sum(
        hamming_distance(data[i * blocksize:(i + 1) * blocksize],
                         data[(i + 1) * blocksize:(i + 2) * blocksize]) / blocksize
        for i in range(n_blocks)
    )
    return hd_normalized / n_blocks

# Dividir bloques y transponerlos
def get_trans_blocks(data, keysize):
    blocks = [data[i:i + keysize] for i in range(0, len(data), keysize)]
    transposed = []
    for i in range(keysize):
        transposed.append(bytearray(block[i] for block in blocks if len(block) > i))
    return transposed

# XOR simple
def single_xor(msg, key):
    return bytes(byte ^ key for byte in msg)

# --- MAIN ---
if __name__ == "__main__":
    try:
        # Leer archivo una vez
        with open(FILENAME, "rb") as file:
            data = file.read()
            data = base64.b64decode(data)

        # Encontrar KEYSIZE óptimo
        keysize_data = {"hamming_distance": math.inf, "keysize": 0}
        for keysize in range(2, 41):
            hd = normalized_hamming_distance(data, keysize)
            if hd < keysize_data["hamming_distance"]:
                keysize_data["hamming_distance"] = hd
                keysize_data["keysize"] = keysize
        
        print(f"The key length is: [{keysize_data['keysize']}]")

        # Dividir en bloques y transponer
        blocks = get_trans_blocks(data, keysize_data["keysize"])

        # Encontrar clave por bloque
        key = bytearray()
        for block in blocks:
            best_score = -math.inf
            best_char = 0
            for candidate in range(256):
                decrypted = single_xor(block, candidate)
                score = english_score(decrypted)
                if score > best_score:
                    best_score = score
                    best_char = candidate
            key.append(best_char)

        print(f"The key is: [{key.decode('latin1')}]")

        # Decodificar el texto usando la clave encontrada
        decrypted_data = bytearray(len(data))
        for i, byte in enumerate(data):
            decrypted_data[i] = byte ^ key[i % len(key)]

        print("====== Texto decodificado ======")
        print(decrypted_data.decode('ascii', errors='ignore'))

    except Exception as e:
        print(f"Error: {e}")
