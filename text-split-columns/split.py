import sys

chunklen = 16

with open(sys.argv[1], 'r') as myfile:
    for line in myfile.readlines():
        print '\n'.join(['%d %s' % (i, line[i:i+chunklen]) for i in range(0, len(line), chunklen)])
