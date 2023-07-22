package main

import (
	"sync"
)

func main() {
	cnt := 0

	var wg sync.WaitGroup

	wg.Add(1)
	go func() {
		defer wg.Done()
		for i := 0; i < 1_000_000; i++ {
			cnt++
		}
	}()

	wg.Add(1)
	go func() {
		defer wg.Done()
		for i := 0; i < 1_000_000; i++ {
			cnt++
		}
	}()

	wg.Wait()
	println(cnt)
}
