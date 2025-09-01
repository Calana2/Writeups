# An ECB/CBC detection oracle 

<img width="1018" height="458" alt="2025-09-01-104641_1018x458_scrot" src="https://github.com/user-attachments/assets/157906fc-e07f-4a38-8a7c-a4a50e61bfc5" />

Seguimos las instrucciones para crear un oraculo de relleno y un oraculo de deteccion. 

El oraculo de deteccion usa la funcion del reto 8 del set 1 para detectar cifrado en modo ECB. En caso contrario asume que el modo usado fue CBC.

Se usa un mensaje con al menos dos bloques completos del mismo byte ("A" * 32) para forzar un bloque duplicado y poder detectar ECB. Debido al padding aleatorio de 5-10 bytes al principio el peor escenario es en el que se usan 5 bytes de padding:
```
xxxxxAAAAAAAAAAA
AAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAA
xxxxx....
```

Como se ve con "A" * 32 + "A" * 11 = "A" * 43 para completar el bloque con el relleno. En el mejor caso se agregan 5 bytes mas lo cual desplaza las "A"es de relleno pero aun quedan dos bloques iguales.
```
xxxxxxxxxxAAAAAA
AAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAA
AAAAAxxxxx....
```

## Solucion en Go
``` go
package main

import (
	"bytes"
	"crypto/aes"
	"fmt"
	"math/rand"
	"os"
)


func xor(var1 []byte, var2 []byte) []byte {
  result := make([]byte, len(var1))
  if len(var1) != len(var2) {
    return nil
  }
  for i:=0; i < len(var1); i++ {
    result[i] = var1[i] ^ var2[i]
  }
  return result
}

func pkcs7Pad(data []byte) []byte {
    padLen := 16 - (len(data) % 16)
    padding := bytes.Repeat([]byte{byte(padLen)}, padLen)
    return append(data, padding...)
}

func AES_ECB_Encrypt(key []byte, input []byte) []byte {
  // Create cipher
  c,err := aes.NewCipher(key)
  if err != nil {fmt.Println(err); os.Exit(1)}
  // Encrypt
  output := make([]byte,len(input))
  for i, j:= 0,16 ; i < len(input); i,j = i+16, j+16 {
    c.Encrypt(output[i:j],input[i:j])
  }
  return output
}

func AES_CBC_Encrypt(iv []byte, key []byte, input []byte) []byte {
  // Create cipher
  c,err := aes.NewCipher(key)
  if err != nil {fmt.Println(err); os.Exit(1)}
  // Encrypt
  previousBlock := iv
  output := make([]byte,len(input))
  for i, j:= 0,16 ; i < len(input); i,j = i+16, j+16 {
    c.Encrypt(output[i:j],xor(input[i:j],previousBlock))
    previousBlock = output[i:j]
  }
  return output
}

func PaddingOracle(input []byte) (ciphertext []byte,mode string) {
  // Generate key
  f, err := os.Open("/dev/urandom")
  if err != nil {fmt.Println(err); os.Exit(1)}
  key := make([]byte,16)
  f.Read(key)
  // Append random padding [5,10] ytes
  bpad := make([]byte,rand.Intn(6) + 5) 
  f.Read(bpad)
  apad := make([]byte,rand.Intn(6) + 5) 
  f.Read(apad)
  plaintext := append(append(bpad, input...),apad...)
  // PKCS#7 padding
  plaintext = pkcs7Pad(plaintext)
  // Random encryption
  if rand.Intn(2) == 0 {
    //fmt.Println("[!] Using AES-ECB...")
    //fmt.Printf("[!] Padded plaintext: %x\n",plaintext)
    //fmt.Printf("[!] Generating random key... (0x%x)\n",key)
    ciphertext = AES_ECB_Encrypt(key,plaintext) 
    mode = "ECB"
  } else {
    //fmt.Println("[!] Using AES-CBC...")
    iv := make([]byte,16)
    f.Read(iv)
    //fmt.Printf("[!] Padded plaintext: %x\n",plaintext)
    //fmt.Printf("[!] Generating random key... (0x%x)\n",key)
    //fmt.Printf("[!] Generating random IV... (0x%x)\n",iv)
    ciphertext = AES_CBC_Encrypt(iv,key,plaintext)
    mode = "CBC"
  }
  // End
  //fmt.Printf("[!] Done. Ciphertext: 0x%x\n\n",ciphertext)
  return ciphertext, mode
}

func detectAESInECBMode(data []byte, keySize int) bool {
 blocks := make(map[string]bool) 
 for i:=0; i<len(data); i+=keySize{
   block := data[i:i+keySize]
   if blocks[string(block)] {
     return true
   }
   blocks[string(block)] = true
 }
 return false
}

func main() {
  var isECB bool
  var hits int
  var numProbes = 1000
  for i:=0; i<numProbes; i++ {
    message,mode := PaddingOracle(bytes.Repeat([]byte("A"), 43))
    isECB = detectAESInECBMode(message,16)
    if (isECB && mode == "ECB") || (!isECB && mode == "CBC") {
     hits++ 
    }
  }
  fmt.Println("[!] Executing Detection Oracle...")
  fmt.Printf("Efectiveness: %.2f%%\n", float64(hits) / float64(numProbes) * 100)
}
```



