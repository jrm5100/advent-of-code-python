#!/usr/bin/python3

##############
# Load input #
##############

grid_serial_number = 7989

##############
# Solution 1 #
##############

def calc_cell_power(x, y, grid_serial_number):
    rack_id = x + 10
    power = rack_id * y
    power += grid_serial_number
    power *= rack_id
    power = int(str(power)[-3])  # Hundreds digit
    power -= 5
    return power

def get_3x3_total(x, y, power_grid):
    """Get the power grid sum for the 3x3 square starting at (x, y) in 1-based coordinates"""
    total = 0
    for i in range(3):
        for j in range(3):
            total += power_grid[x+i-1][y+j-1]
    return total

power_grid = [[calc_cell_power(x, y, grid_serial_number) for y in range(1, 301)] for x in range(1, 301)]

best_coord = None
max_power = -5 * 9
for x in range(1, 299):
    for y in range(1, 299):
        power = get_3x3_total(x, y, power_grid)
        if power > max_power:
            best_coord = (x, y)
            max_power = power
            print(best_coord, max_power)

answer = best_coord
print(f"Solution to part 1 is {answer}")

##############
# Solution 2 #
##############

# Lots of room for optimization with added complexity (or using numpy)
#  -> create a grid of small squares and build them up their power into large squares
#  -> calculate the maximum possible power in a position and skip full calculation when a better square total isn't possible
#  -> Break down the formula to find a pattern based on x-position and y-positions

def get_square_total(x, y, power_grid):
    """Get the max power grid sum for the squares starting at (x, y) in 1-based coordinates"""
    total = power_grid[x-1][y-1]
    best_total = total
    best_size = 1

    # Expand square, choosing better totals
    for size in range(2, 300):
        if x + size > 300 or y + size > 300:
            # Return current best if overlapping an edge
            return best_size, best_total
        else:
            for nx in range(x-1, x-1 + size):  # for example, range(0, 2) for a size of 2
                total += power_grid[nx][y-1 + size-1]  # subtract 1 from size to correct for indexing, not needed in range function
            for ny in range(y-1, y-1 + size - 1):  # Range is smaller by 1 to skip last row in column since it was already counted
                total += power_grid[x-1 + size-1][ny]
        # Update best result so far
        if total > best_total:
            best_total = total
            best_size = size
    
    # Return best after checking all squares
    return best_size, best_total

best_coord = None
max_power = -5
for x in range(1, 299):
    for y in range(1, 299):
        size, power = get_square_total(x, y, power_grid)
        if power > max_power:
            best_coord = (x, y, size)
            max_power = power
            print(best_coord, max_power)

answer = best_coord
print(f"Solution to part 2 is {answer}")
