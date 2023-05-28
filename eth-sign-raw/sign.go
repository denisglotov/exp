// Sign data as is, no EIP-191 prefox added
// Inspired by https://goethereumbook.org/signature-generate/

package main

import (
	"fmt"
	"log"
	"os"
	"strings"

	"github.com/ethereum/go-ethereum/common/hexutil"
	"github.com/ethereum/go-ethereum/crypto"
)

func main() {
	privateKeyStr := os.Getenv("PRIV")
	if strings.HasPrefix(privateKeyStr, "0x") {
		privateKeyStr = privateKeyStr[2:]
	}
	privateKey, err := crypto.HexToECDSA(privateKeyStr)
	if err != nil {
		log.Fatal(err)
	}

	data := make([]byte, 3*32)
	data[31] = 2
	data[63] = 1
	hash := crypto.Keccak256Hash(data)
	fmt.Println("hash =", hash.Hex())

	signature, err := crypto.Sign(hash.Bytes(), privateKey)
	if err != nil || len(signature) != 65 {
		log.Fatal(err)
	}

	r := signature[0:32]
	s := signature[32:64]
	v := signature[64] + 0x1b

	fmt.Println("v =", hexutil.Encode([]byte{v}))
	fmt.Println("r =", hexutil.Encode(r))
	fmt.Println("s =", hexutil.Encode(s))
}

/*
0x1b
0xb2f73c3b85f01b6ade5e1b0cef3a062cb7c9e21684725e133acfc011656ddd7d
0x1400dbb625bd34f65c97e0673b2a5a705c2f5d357e7c877de6f0334c7224de4a
0x0000000000000000000000000000000000000000000000000000000000000001
0x0000000000000000000000000000000000000000000000000000000000000000
*/
