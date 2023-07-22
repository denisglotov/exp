// Run: go test -v ./race_benchmark_test.go -bench .

package main

import (
	"sync"
	"sync/atomic"
	"testing"
)

const Iterations = 1000
const Parallels = 8

func incAtomic() int {
	cnt := int32(0)

	var wg sync.WaitGroup

	for i := 0; i < Parallels; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for i := 0; i < Iterations; i++ {
				atomic.AddInt32(&cnt, 1)
			}
		}()
	}

	wg.Wait()
	return int(cnt)
}

func BenchmarkIncAtomic(b *testing.B) {
	for i := 0; i < b.N; i++ {
		incAtomic()
	}
}

func incMutex() int {
	cnt := int32(0)

	var wg sync.WaitGroup
	var mu sync.Mutex

	for i := 0; i < Parallels; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for i := 0; i < Iterations; i++ {
				mu.Lock()
				cnt++
				mu.Unlock()
			}
		}()
	}

	wg.Wait()
	return int(cnt)
}

func BenchmarkIncMutex(b *testing.B) {
	for i := 0; i < b.N; i++ {
		incMutex()
	}
}

func main() {
	println(incAtomic())
	println(incMutex())
}
