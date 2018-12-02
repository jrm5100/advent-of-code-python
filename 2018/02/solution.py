#!/usr/bin/python3

from collections import Counter

# Load input
with open("input.txt", "r") as f:
    ids = [l.strip() for l in f]

# Solution 1

# Could be faster to make the counter objects once?
two_letter_ids = [id for id in ids if 2 in Counter(id).values()]
three_letter_ids = [id for id in ids if 3 in Counter(id).values()]
checksum = len(two_letter_ids) * len(three_letter_ids)

print(f"Solution to part 1 is {checksum}")

# Solution 2

# Iterate through list, comparing the ID to all IDs after it
matched_id_portion = None
for idx, current_id in enumerate(ids[:-1]):
    for idx2, other_id in enumerate(ids[idx+1:]):
        diff = sum([c != o for c, o in zip(current_id, other_id)])
        if diff == 1:
            matched_id_portion = "".join([c for c, o in zip(current_id, other_id) if c == o])
            break

print(f"Solution to part 2 is {matched_id_portion}")