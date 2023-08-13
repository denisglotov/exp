Data race simulation
====================

Play with it:

* Use race detector:

        go run -race race_with_wait.go

* Run on a single processor:

        GOMAXPROCS=1 go run race_with_wait.go

* Run the benchmark to compare atomics with mutexes:

        go test -v ./race_benchmark_test.go -bench .
