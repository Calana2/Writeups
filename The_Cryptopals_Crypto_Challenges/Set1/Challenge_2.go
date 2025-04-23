package main

import (
	"encoding/hex"
	"fmt"
)

func FixedXOR(s1 string, s2 string) string {
 raw1,_ := hex.DecodeString(s1)
 raw2,_ := hex.DecodeString(s2)
 if (len(raw1) != len(raw2)) {
  return ""
 }
 raw3 := make([]byte,len(raw1))
 for i:=0; i < len(raw1); i++ {
   raw3[i] = raw1[i] ^ raw2[i]
 }
 return hex.EncodeToString(raw3)
}


func main(){
  s1 := "1c0111001f010100061a024b53535009181c"
  s2 := "686974207468652062756c6c277320657965"
  s3 := FixedXOR(s1,s2)
  fmt.Println(s3)
}
