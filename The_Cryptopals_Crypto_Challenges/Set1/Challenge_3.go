package main

import (
	"encoding/hex"
	"fmt"
)

func isASCIIPrintable(b []byte) bool{
 for _,val := range b {
   if val < 32 || val > 126 {
     return false
   }
 }
 return true
}

func main() {
  raw_str,_ := hex.DecodeString("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736")
  for k := 0; k <= 255; k++ {
    guessed := make([]byte,len(raw_str))
    // Realizar XOR con el texto cifrado y la clave actual
    for i := 0; i < len(raw_str); i++ {
    guessed[i] = raw_str[i] ^ byte(k)
   }
   // Mostrar texto que solo contenga ASCII imprimible
   if isASCIIPrintable(guessed) {
     fmt.Printf("key='%c': text=%s\n",rune(k) ,string(guessed))
   }
  }
}
