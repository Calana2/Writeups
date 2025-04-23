package main

import (
	"crypto/aes"
	"encoding/base64"
	"fmt"
	"os"
)

func AES_ECB_Decrypt(key, data []byte) (string, error) {
 ciph, err := aes.NewCipher(key)
 if err != nil {
   return "",err
 }
 blockSize := ciph.BlockSize()
 plaintext := make([]byte,len(data))
 for i,j := 0,blockSize; i < len(data); i,j = i+blockSize,j+blockSize {
   ciph.Decrypt(plaintext[i:j],data[i:j])
 }
 return string(plaintext),nil
}

func main() {
  b64_data,err := os.ReadFile("7.txt")
  if err != nil {
    fmt.Println(err)
    return
  }
  raw_data := make([]byte,len(b64_data))
  l,err := base64.RawStdEncoding.Decode(raw_data,b64_data)
  if err != nil {
    fmt.Println(err)
    return
  }
  key := []byte("YELLOW SUBMARINE")
  plaintext, err := AES_ECB_Decrypt(key,raw_data[:l])
  if err != nil {
    fmt.Println(err)
    return
  }
  fmt.Println(plaintext)
}
