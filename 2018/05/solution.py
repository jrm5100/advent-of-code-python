#!/usr/bin/python3

##############
# Load input #
##############

# Get event messages sorted by time

with open("input.txt", "r") as f:
    polymer = f.read().strip()

def react(left, right):
    if left.upper() != right.upper():
        return False
    elif left.islower() and right.isupper():
        return True
    elif left.isupper() and right.islower():
        return True
    else:
        return False

def collapse_polymer(polymer: str) -> str:
    """Remove components that interact with one another and return the result"""
    polymer = [c for c in polymer]
    i = 0
    while i < len(polymer)-1:
        if react(polymer[i], polymer[i+1]):
            # Delete the reacted ones and go back one space (if possible) to look for newly created reaction pairs
            del polymer[i:i+2]
            if i > 0:
                i -= 1
        else:
            i += 1
    return "".join(polymer)



##############
# Solution 1 #
##############

collapsed_polymer = collapse_polymer(polymer)
print(f"Solution to part 1 is {len(collapsed_polymer)}")

##############
# Solution 2 #
##############

# This is a brute force solution (there is probably a faster way) but ~6 seconds is good enough.
lowest_len = len(polymer)
for c in "abcdefghijklmnopqrstuvwxyz":
    test_polymer = polymer.replace(c, '').replace(c.upper(), '')
    test_polymer = collapse_polymer(test_polymer)
    if len(test_polymer) < lowest_len:
        lowest_len = len(test_polymer)

print(f"Solution to part 2 is {lowest_len}")
