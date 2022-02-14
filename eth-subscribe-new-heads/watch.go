// Based on https://goethereumbook.org/event-subscribe/

package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"

	"github.com/ethereum/go-ethereum/core/types"
	"github.com/ethereum/go-ethereum/ethclient"
)

func main() {
	log.Println("Connecting...")

	client, err := ethclient.Dial("wss://bsc-ws-node.nariox.org:443")
	if err != nil {
		log.Fatal(err)
	}

	logs := make(chan *types.Header)
	sub, err := client.SubscribeNewHead(context.Background(), logs)
	if err != nil {
		log.Fatal(err)
	}
	defer sub.Unsubscribe()

	for {
		select {
		case err := <-sub.Err():
			log.Fatal(err)
		case vLog := <-logs:
			raw, _ := json.Marshal(vLog)
			fmt.Println(string(raw))
		}
	}
}
