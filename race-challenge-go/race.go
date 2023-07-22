package main

func main() {
	cnt := 0

	go func() {
		for i := 0; i < 1_000_000; i++ {
			cnt++
		}
	}()

	go func() {
		for i := 0; i < 1_000_000; i++ {
			cnt++
		}
	}()

	println(cnt)
}
