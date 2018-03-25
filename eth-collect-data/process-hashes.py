import re
import sys

buckets = [0] * 1000
hash_matcher = re.compile(r'^\s*"hash": "(0x[a-fA-F0-9]+)"')
for line in sys.stdin:
    match = hash_matcher.match(line)
    if match:
        hash = int(match.group(1), 16)
        buckets[hash % 1000] += 1

print ', '.join([str(bucket) for bucket in buckets])
