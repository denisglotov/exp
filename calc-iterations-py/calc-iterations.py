import sys

def funk(n, shift, ctr):
    print(". " * shift, n)
    ctr += 1
    for i in range(n):
        ctr = funk(n - i - 1, shift + 1, ctr)
    return ctr

print(funk(int(sys.argv[1]), 0, 0))
