package main

import (
	"bytes"
	"fmt"
)

// Lo se, es muy verboso

func pad(chunk []byte, block_size int) ([]byte,error) {
  if len(chunk) > block_size {
    return nil,fmt.Errorf("Longitud del bloque  mayor que lo esperado.")
  }
  plen := block_size - (len(chunk) % block_size)
  pad := bytes.Repeat([]byte{byte(plen)}, plen)
  return append(chunk, pad...),nil
}

func unpad(pchunk []byte) ([]byte, error) {
  plen := int(pchunk[len(pchunk)-1])
  pad := bytes.Repeat([]byte{byte(plen)}, plen)
  if !bytes.Equal(pchunk[len(pchunk)-plen:],pad) {
    return nil,fmt.Errorf("Padding invalido.")
  }
  return pchunk[:len(pchunk)-plen],nil
}

func main() {
  padded,_ := pad([]byte("YELLOW SUBMARINE"),20)
  unpadded,_ := unpad(padded)
  fmt.Println(padded)
  fmt.Println(unpadded)
}
