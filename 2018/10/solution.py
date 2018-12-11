#!/usr/bin/python3

# Note: this solution is more interactive, given the limited ways of calculating a precise mathematical solution

##############
# Load input #
##############

points = []
with open("input.txt", "r") as f:
    for line in f:
        x = int(line.split('<')[1].split(',')[0])
        y = -1 * int(line.split(',')[1].split('>')[0])
        vx = int(line.split('<')[2].split(',')[0])
        vy = -1 * int(line.split(',')[2].split('>')[0])
        points.append(dict(x=x, y=y, vx=vx, vy=vy))

##############
# Solution 1 #
##############

def update_points(points):
    for p in points:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
    return points

def print_grid(points):
    # Get the range
    xlist = [p["x"] for p in points]
    ylist = [p["y"] for p in points]
    xmin = min(xlist)
    xmax = max(xlist)
    ymin = min(ylist)
    ymax = max(ylist)

    grid = []
    for i in range(ymin, ymax+1):
        xpoints = [p["x"] for p in points if p["y"] == i]
        grid.append("".join(['.' if n not in xpoints else '#' for n in range(xmin, xmax+1)]))
    # Must reverse to get the y-order back to the original orientation
    for row in grid[::-1]:
        print(row)

unique_x = set([p["x"] for p in points])
unique_y = set([p["y"] for p in points])

passed_seconds = 0
# Skip ahead until they are more lined up
while len(unique_x) > 50 and len(unique_y) > 50:
    points = update_points(points)
    passed_seconds += 1
    unique_x = set([p["x"] for p in points])
    unique_y = set([p["y"] for p in points])

while True:
    print(f"----- {passed_seconds:,} seconds passed -----")
    print_grid(points)
    input()
    points = update_points(points)
    passed_seconds += 1
