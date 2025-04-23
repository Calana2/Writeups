package main

import (
	"encoding/base64"
	"encoding/hex"
	"fmt"
)

func main() {
  hexstr := "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
  raw,_ := hex.DecodeString(hexstr)
  base64Text := base64.StdEncoding.EncodeToString(raw)
  fmt.Println(base64Text)
}
