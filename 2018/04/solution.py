#!/usr/bin/python3

from datetime import datetime

datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')

##############
# Load input #
##############

# Get event messages sorted by time

events = []
with open("input.txt", "r") as f:
    for line in f:
        dt = datetime.strptime(line[:18], '[%Y-%m-%d %H:%M]')
        message = line[19:].strip()
        events.append((dt, message))
events = sorted(events, key=lambda t: t[0])

# Use a dict of lists that count how many times the guard slept in that minute
nap_mins_dict = dict()
for e in events:
    if "Guard" in e[1]:
        # Note the guard ID and add it to the dict of guards if it isn't already present
        guard_id = int(e[1].split(" ")[1][1:])
        if guard_id not in nap_mins_dict:
            nap_mins_dict[guard_id] = [0]*60  # Initialze to a 60 (min) length array of 0s
    elif e[1] == "falls asleep":
        # Record nap_start
        nap_start = e[0].minute
    elif e[1] == "wakes up":
        # Record which minutes were naps
        for i in range(nap_start, e[0].minute):
            nap_mins_dict[guard_id][i] += 1

##############
# Solution 1 #
##############

# Figure out the answer
max_time = 0
sleepiest_guard = None
sleepiest_minute = None
for guard_id, nap_array in nap_mins_dict.items():
    total = sum(nap_array)
    if total > max_time:
        max_time = total
        sleepiest_guard = guard_id
        sleepiest_minute = nap_array.index(max(nap_array))  # Doesn't matter if a few minutes tie, pick the first

print(f"Solution to part 1 is {sleepiest_guard * sleepiest_minute}")

##############
# Solution 2 #
##############

# Figure out the answer
max_time = 0
sleepiest_guard = None
sleepiest_minute = None
for guard_id, nap_array in nap_mins_dict.items():
    most_naps = max(nap_array)
    if most_naps > max_time:
        max_time = most_naps
        sleepiest_guard = guard_id
        sleepiest_minute = nap_array.index(max(nap_array))  # Doesn't matter if a few minutes tie, pick the first

print(f"Solution to part 2 is {sleepiest_guard * sleepiest_minute}")
