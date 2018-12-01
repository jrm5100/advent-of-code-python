#!/usr/bin/python3

# Load input
with open("input.txt", "r") as f:
    changes = [int(l.strip()) for l in f]

# Solution 1
print(f"Solution to part 1 is {sum(changes)}")

# Solution 2
import collections

changes = collections.deque(changes)
previous_frequencies = set()
current = changes[0]
while current not in previous_frequencies:
    previous_frequencies.add(current)
    changes.rotate(-1)
    current += changes[0]

print(f"Solution to part 2 is {current}")
