//go:build integration
// +build integration

package test

import "log"

func init() {
	log.Print("Hello world!")
}

func calc() int {
	return 2 + 2
}
