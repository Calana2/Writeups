package main

import (
	"encoding/hex"
	"fmt"
)

func XOR_encrypt(msg []byte, key []byte) ([]byte, error) {
  result := make([]byte,len(msg))
  if len(msg) < len(key) {
    return nil, fmt.Errorf("Key must be less or equal than the message")
  }
  key_index := 0
  for i:=0; i < len(msg); i++ {
    result[i] = msg[i] ^ key[key_index]
    key_index = (key_index+1) % len(key)
  }
  return result,nil
}

func main() {
  message := []byte("Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal")
  key := []byte("ICE")
  result,err := XOR_encrypt(message,key)
  if err != nil {
    fmt.Println("Error: ",err)
    return
  }
  fmt.Println(hex.EncodeToString(result))
}
