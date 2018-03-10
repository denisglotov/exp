import sys

print sys.argv

str = ''
with open(sys.argv[1], 'rb') as inp:
    while True:
        c = inp.read(1)
        if not c:
            break
        if c != '\n':
            str += c
print 'Accepted %d digits.\n' % len(str)

open(sys.argv[2], 'wb').write(str.strip().decode('hex'))
