package main

import (
	"encoding/hex"
	"fmt"
	"os"
	"strings"
)

func detectAESInECBMode(data []byte, keySize int) bool {
  blocks := make(map[string]bool)
  for i:=0; i<len(data); i+=16 {
   block := string(data[i:i+keySize])
   if blocks[block] {
     return true
   }
   blocks[block] = true
  }
  return false
}

func detectECBFile(lines []string) (int,[]byte,error) {
  for num, line := range lines {
		decoded, err := hex.DecodeString(line)
		if err != nil {
			return 0,nil,err
		}
		if detectAESInECBMode(decoded, 16) {
			return num,decoded, nil
		}
  }
  return 0,nil,fmt.Errorf("No AES-ECB ciphertext found")
}

func main() {
  file,err := os.ReadFile("8.txt")
  lines := strings.Split(string(file),"\n")
  if err != nil {
   fmt.Println(err)
   return
  }
  lineNum, data, err := detectECBFile(lines)
  if err != nil {
    fmt.Println(err)
  }
  fmt.Println("Block whit AES-ECB found:")
  fmt.Printf("%d:   %s\n",lineNum,hex.EncodeToString(data))
}
