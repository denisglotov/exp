#!/usr/bin/python
#
# GDB extension to find and substitute magic signatures in the attached
# process.
#
# Use: sudo gdb -q --batch --command ~/exp/magic-replace.py --pid ${PID}
#
import re
import gdb

MAGIC = "'H', 'a', 'c', 'k', 'M', 'e', 'H', 'e'"

stats = gdb.execute("info proc stat", False, True)
for stat in stats.splitlines():
    if stat.startswith("Process:"):
        pid = int(stat.split(':')[1])
        break
print("Working with PID", pid)

# 'info proc mappings' does not have access rights so use /proc/./maps.
with open("/proc/%d/maps" % pid, 'r') as maps_file:
    for line in maps_file.readlines():
        region_printed = False
        line = line.strip()
        mem = re.match(r'^([0-9A-Fa-f]+)-([0-9A-Fa-f]+) ([-r][-w])', line)
        if mem.group(3) == "rw":
            first = int(mem.group(1), 16)
            last = int(mem.group(2), 16) - 1
            spots = gdb.execute("find 0x%X, 0x%X, %s" % (first, last, MAGIC), False, True)
            for spot in spots.splitlines():
                spot_match = re.match(r'^0x([0-9A-Fa-f]+)', spot)
                if spot_match:
                    spot_addr = int(spot_match.group(1), 16)
                    if not region_printed:
                        print("In memory region '%s'" % line)
                        region_printed = True
                    print("  processing %X" % spot_addr)
                    gdb.execute("set {int}0x%X = 0" % spot_addr)

print("Detaching the process %d." % pid)
gdb.execute("detach", False)
