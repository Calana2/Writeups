package main

import (
	"bytes"
	"encoding/base64"
	"fmt"
	"math"
	"os"
)

// English score
var english_frequencies = map[byte]float64{
	'E': 12.02, 'T': 9.10, 'A': 8.12, 'O': 7.68, 'I': 7.31, 'N': 6.95,
	'S': 6.28, 'H': 6.09, 'R': 5.99, 'D': 4.32, 'L': 4.03, 'U': 2.88,
	'C': 2.71, 'M': 2.61, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'P': 1.82,
	'Y': 1.75, 'B': 1.49, 'V': 1.11, 'K': 0.69, 'X': 0.17, 'J': 0.10,
	'Q': 0.10, 'Z': 0.07, ' ': 13.00,
}

func scoreText(text []byte) float64 {
	score := 0.0
	total_letters := 0
  letter_count := make(map[byte]float64)
	for _, c := range text {
		// Convertir a mayúscula y buscar en frecuencias
		char := bytes.ToUpper([]byte{c})[0]
		if _, ok := english_frequencies[char]; ok {
			letter_count[char] += 1
			total_letters += 1
		}
	}
	if total_letters != 0 {
    // Puntuar usando chi-cuadrado
		for char, observed := range letter_count {
			expected := english_frequencies[char] * float64(total_letters)
			diff := observed - expected
			score += (diff * diff) / expected
		}
	}

	return score
}

// Bit difference measure
func Hamming_distance(a []byte, b []byte) (int, error) {
	if len(a) != len(b) {
		return 0, fmt.Errorf("Params must have the same length ")
	}
	distance := 0
	for i := 0; i < len(a); i++ {
		xor := a[i] ^ b[i]
		for xor != 0 {
			distance += int(xor & 1)
			xor >>= 1
		}
	}
	return distance, nil
}

func main() {
	// Leer el archivo
	f, err := os.ReadFile("6.txt")
	data := make([]byte, len(f))
	if err != nil {
		fmt.Println("Error reading the file: ", err)
		return
	}
  // Decodificar base64
  decodeLen, err := base64.StdEncoding.Decode(data, f)
	if err != nil {
		fmt.Println("Error decoding the file: ", err)
		return
	}
  data = data[:decodeLen]

	// Encontrar el mejor keysize
	best_keysize := 2
	min_normalized_distance := math.MaxFloat64
	for KEYSIZE := 2; KEYSIZE <= 40; KEYSIZE++ {
		num_blocks := 10
		total_hd := 0

		for i := 0; i < num_blocks; i++ {
			block1 := data[i*KEYSIZE : (i+1)*KEYSIZE]
			block2 := data[(i+1)*KEYSIZE : (i+2)*KEYSIZE]
			hd, _ := Hamming_distance(block1, block2)
			total_hd += hd
		}

		normalized_distance := float64(total_hd) / float64(KEYSIZE*num_blocks)

		if normalized_distance < min_normalized_distance {
			min_normalized_distance = normalized_distance
			best_keysize = KEYSIZE
		}
	}

	// Dividir el texto en KEYSIZE 29
	var blocks [][]byte
	for i := 0; i < len(data); i += best_keysize {
		end := i + best_keysize
		if end > len(data) {
			end = len(data)
		}
		blocks = append(blocks, data[i:end])
	}

	// Transponer los bloques
	var transposed [][]byte
	for i := 0; i < best_keysize; i++ {
		var newBlock []byte
		for _, block := range blocks {
			if i < len(block) {
				newBlock = append(newBlock, block[i])
			}
		}
		transposed = append(transposed, newBlock)
	}

	// Probar cada byte como clave de cada bloque y puntuar
	var key []byte
	for _, block := range transposed {
		bestScore := 0.0
		bestByte := byte(0)
		for i := 0; i <= 255; i++ {
			candidate := byte(i)
			// XOR
			decrypted := make([]byte, len(block))
			for j := range block {
				decrypted[j] = block[j] ^ candidate
			}
			// Puntuar
			score := scoreText(decrypted)
			if score > bestScore {
				bestScore = score
				bestByte = candidate
			}
		}
		key = append(key, bestByte)
	}
	fmt.Println("====== Clave encontrada ======\n", string(key))

	// Decodificar el texto con la clave
	decrypted := make([]byte, len(data))
	for i := range data {
		decrypted[i] = data[i] ^ key[i%len(key)]
	}
	fmt.Println("====== Texto decodificado ======\n", string(decrypted))
}
