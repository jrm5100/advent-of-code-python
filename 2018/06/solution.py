#!/usr/bin/python3

from collections import namedtuple

##############
# Load input #
##############

coordinate = namedtuple("Coordinate", ["x", "y"])
coordinates = []
with open("input.txt", "r") as f:
    for line in f:
        x, y = line.strip().split(", ")
        coordinates.append(coordinate(x=int(x), y=int(y)))

print(coordinates)


##############
# Solution 1 #
##############

answer = ""
print(f"Solution to part 1 is {answer}")

##############
# Solution 2 #
##############

answer = ""
print(f"Solution to part 2 is {answer}")
