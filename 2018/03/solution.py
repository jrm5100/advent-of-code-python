#!/usr/bin/python3

from collections import defaultdict
from dataclasses import dataclass

# Load input

@dataclass
class Claim:
    '''Class for keeping track of a claimed region'''
    name: int
    x: int
    y: int
    width: int
    height: int

claims = []
with open("input.txt", "r") as f:
    for line in f:  # line = #123 @ 3,2: 5x4
        line = line[1:].replace("@ ", "").replace(":", "") # line = 123 3,2 5x4
        name, pos, size = line.split(" ")
        
        name = int(name)
        x, y = [int(n) for n in pos.split(",")]
        width, height = [int(n) for n in size.split("x")]
        
        claims.append(Claim(name, x, y, width, height))

# Solution 1
# Only track positions that are in claims since the cloth is of indeterminant size and may be like a sparse array anyway

cloth = defaultdict(list)
for claim in claims:
    for i in range(claim.width):
        for j in range(claim.height):
            position = (claim.x + i, claim.y + j)
            cloth[position].append(claim.name)

overlap_positions = sum([1 for claim_list in cloth.values() if len(claim_list) > 1 ])

print(f"Solution to part 1 is {overlap_positions}")

# Solution 2
# This is a simple solution starting with all claims and iteratively removing those with overlaps

non_overlapped_claim_names = set(claim.name for claim in claims)
for v in cloth.values():
    if len(v) > 1:
        # Remove any claim names that are in this overlap position
        non_overlapped_claim_names = non_overlapped_claim_names - set(v)
# Trust that there is only 1 non-overlapped like it says
print(f"Solution to part 2 is {non_overlapped_claim_names.pop()}")
