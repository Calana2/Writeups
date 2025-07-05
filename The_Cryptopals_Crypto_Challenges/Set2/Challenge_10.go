package main

import (
	"bytes"
	"crypto/aes"
	"encoding/base64"
	"fmt"
	"os"
)

func XOR(var1 []byte, var2 []byte) ([]byte, error) {
  result := make([]byte, len(var1))
  if len(var1) != len(var2) {
    return nil, fmt.Errorf("Params must have the same length")
  }
  for i:=0; i < len(var1); i++ {
    result[i] = var1[i] ^ var2[i]
  }
  return result,nil
}


func AES_ECB_Decrypt(key, data []byte) ([]byte, error) {
 ciph, err := aes.NewCipher(key)
 if err != nil {
   return nil,err
 }
 blockSize := ciph.BlockSize()
 plaintext := make([]byte,len(data))
 for i,j := 0,blockSize; i < len(data); i,j = i+blockSize,j+blockSize {
   ciph.Decrypt(plaintext[i:j],data[i:j])
 }
 return plaintext,nil
}

func AES_CBC_Decrypt(key, iv, data []byte) ([]byte, error) {
 blockSize := 16
 plaintext := make([]byte,len(data))
 previousBlock := iv
 for i,j := 0,blockSize; i < len(data); i,j = i+blockSize,j+blockSize {
   current_block := data[i:j]
   decrypt,err := AES_ECB_Decrypt(key,current_block)
   if err != nil {
     return nil,err
   }
   plaintext_block,err := XOR(decrypt,previousBlock)
   plaintext = append(plaintext, plaintext_block...)
   previousBlock = current_block
 }
 return plaintext,nil
}

func main() {
  b64_data,err := os.ReadFile("10.txt")
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
  iv := bytes.Repeat([]byte{byte(0x30)},16)
  plaintext, err := AES_CBC_Decrypt(key,iv,raw_data[:l])
  if err != nil {
    fmt.Println(err)
    return
  }
  fmt.Println(string(plaintext))
}
