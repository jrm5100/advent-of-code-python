#!/usr/bin/python3

from collections import Counter

##############
# Load input #
##############

coordinates = []
with open("input.txt", "r") as f:
    for line in f:
        x, y = line.strip().split(", ")
        coordinates.append((int(x), int(y)))

# Shift coordinates to make indexing easier
shift_x = min([c[0] for c in coordinates])
shift_y = min([c[1] for c in coordinates])
coordinates = [(c[0]-shift_x, c[1]-shift_y) for c in coordinates]

def calc_distance(x1, y1, x2, y2):
    return abs(x1-x2) + abs(y1-y2)

# Create a 3D matrix indexed by coordinate, x, y that lists the distance from x, y to that coordinate
max_x = max([c[0] for c in coordinates])
max_y = max([c[1] for c in coordinates])
distance_matrix = []
for coordinate_idx, coordinate in enumerate(coordinates):
    current_layer = []
    for i in range(max_x + 1):
        # Append one row of distance at a time
        current_layer.append([calc_distance(coordinate[0], coordinate[1], i, j) for j in range(max_y + 1)])
    distance_matrix.append(current_layer)

##############
# Solution 1 #
##############

# Assign closest-position to each x-y coordinate
labels = []
for i in range(max_x + 1):
    labels.append([])
    for j in range(max_y + 1):
        distances = [l[i][j] for l in distance_matrix]
        min_distance = min(distances)
        if distances.count(min_distance) > 1:
            labels[i].append(-1)
        else:
            labels[i].append(distances.index(min_distance))

# Get total area for each
area_dict = Counter()
for row in labels:
    area_dict += Counter(row)

# Remove any that appear in the border
for k, v in area_dict.items():
    if k in labels[0] or k in labels[-1]:
        area_dict[k] = 0
    if k in [row[0] for row in labels] or k in [row[-1] for row in labels]:
        area_dict[k] = 0

# Answer is the remaining largest area
coordinate_idx, largest_area = area_dict.most_common(1)[0]
print(f"Solution to part 1 is {largest_area}")

##############
# Solution 2 #
##############

# Calculate sum of distances to all coordinates for each point
count = 0
for i in range(max_x + 1):
    for j in range(max_y + 1):
        distances = [l[i][j] for l in distance_matrix]
        total = sum(distances)
        if total < 10000:
            count += 1

answer = count
print(f"Solution to part 2 is {answer}")
