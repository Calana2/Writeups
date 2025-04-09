# Break repeating-key XOR

![2025-04-09-161339_1061x316_scrot](https://github.com/user-attachments/assets/bef2aee6-2f2a-4f0a-aba5-e0920d7c36a7)

Primero debemos crear y probar una funcion que calcule la distancia de Hamming entre dos cadenas (la sumatoria del numero de bits diferentes entre cada par de bytes):
``` go
package main

import (
  "fmt"
)

// Bit difference measure
func Hamming_distance(a []byte, b []byte) (int, error) {
 if len(a) != len(b) {
  return 0, fmt.Errorf("Params must have the same length ")
 }
 distance := 0
 for i:=0; i<len(a); i++ {
  xor := a[i] ^ b[i]
  for xor != 0 {
   distance += int(xor & 1)
   xor >>= 1
  }
 }
 return distance,nil
}

func main() {
  d,_ := Hamming_distance([]byte("this is a test"),[]byte("wokka wokka!!!"))
  print(d)
}
```

Para los pasos 3 y 4:
``` go
package main

import (
	"encoding/base64"
	"fmt"
	"math"
	"os"
)

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
	_, err = base64.StdEncoding.Decode(data, f)
	if err != nil {
		fmt.Println("Error decoding the file: ", err)
		return
	}

	// Encontrar el mejor keysize
	best_keysize := 2
	min_normalized_distance := math.MaxFloat64
	for KEYSIZE := 2; KEYSIZE <= 40; KEYSIZE++ {
    num_blocks := 10
		total_hd := 0
  /* Comparamos num_blocks bloques de tamaño KEYSIZE
     Hallamos la distancia de Hamming para cada par de bloques y las sumamos */
		for i := 0; i < num_blocks; i++ {
			block1 := data[i*KEYSIZE : (i+1)*KEYSIZE]
			block2 := data[(i+1)*KEYSIZE : (i+2)*KEYSIZE]
			hd, _ := Hamming_distance(block1, block2)
			total_hd += hd
		}
   
    // Dividimos las sumas de las distancias entre el tamaño de bloque * KEYSIZE (normalizacion)
		normalized_distance := float64(total_hd) / float64(KEYSIZE*num_blocks)
		fmt.Printf("KEYSIZE: %d, Normalized HD: %.2f\n", KEYSIZE, normalized_distance)

		if normalized_distance < min_normalized_distance {
      // Buscamos la distancia minima y guardamos el valor de KEYSIZE pmas probable
			min_normalized_distance = normalized_distance
			best_keysize = KEYSIZE
		}
	}
  fmt.Println("Mejor KEYSIZE:", best_keysize)
}
```

Notese que num_blocks esta establecido a 10, porque al principio, si comparaba pocos bloques los KEYSIZES mas probables variaban: 
[`2`,`5`,`29`]

A partir de comparar 10 pares de bloques hasta 30 se mantuvo `29` como el KEYSIZE definitivo

#### Continuar
