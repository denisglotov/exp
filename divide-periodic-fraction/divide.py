# -*- flycheck-python-flake8-executable: "python3" -*-

import sys

try:
    a, b = sys.argv[1:3]
except ValueError:
    print('Specify numerator and denominator as 2 arguments.')
    sys.exit(1)

print(a, '/', b, '=', end=' ')
d = int(a)
b = int(b)
dot_already_put = False

for x in range(100):
    while(d < b):
        d *= 10
        print('0', end='')
        if not dot_already_put:
            print('.', end='')
            dot_already_put = True
    print(int(d / b), end='')
    d = d % b * 10
    if (d == 0):
        break
    if not dot_already_put:
        print('.', end='')
        dot_already_put = True
if (d == 0):
    print()
else:
    print('...')
