package main

import (
	"encoding/hex"
	"fmt"
	"os"
	"strings"
)

func isASCIIPrintable(b []byte) bool{
 for _,val := range b {
   // Tuve que agregar los caracteres de tabulacion(9) y nueva linea(10)
   // porque de no hacerlo eliminaba lineas validas
   if (val < 32 && val != 9 && val != 10) || val > 126  {
     return false
   }
 }
 return true
}

 func XORBruteForceLine(line string, linenum int) {
  raw_str,_ := hex.DecodeString(line)
  var output []string
  for k := 0; k <= 255; k++ {
    guessed := make([]byte,len(raw_str))
    // Realizar XOR con el texto cifrado y la clave actual
    for i := 0; i < len(raw_str); i++ {
    guessed[i] = raw_str[i] ^ byte(k)
   }
   // Mostrar texto que solo contenga ASCII imprimible
   if isASCIIPrintable(guessed) {
     output = append(output, fmt.Sprintf("key='%c': text=%s\n",rune(k) ,string(guessed)))
   }
  }
  if len(output) == 0 {
   return

  }
  fmt.Printf("\n======== LINE %d ========\n",linenum)
  for _,l := range(output) {
   fmt.Println(l)
  }
 }

func main() {
 f,err := os.ReadFile("4.txt")
 if err != nil {
   fmt.Printf("Error reading the file: %s\n",err)
 }
 for n,l := range(strings.Split(string(f),"\n")) {
   XORBruteForceLine(l,n)
 }
}
