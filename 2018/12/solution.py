#!/usr/bin/python3

##############
# Load input #
##############

rules = dict()
with open("input.txt", "r") as f:
    initial_state = f.readline().strip().split(" ")[2]
    f.readline()
    for line in f.readlines():
        rules[line.split(" => ")[0]] = line.strip().split(" => ")[1]

##############
# Solution 1 #
##############

current_state = "...." + initial_state + "...." # Pad out non-plants on either end
for step in range(20):
    new_state = ""
    for idx in range(len(current_state)-4):  # Iterate as far as possible
        new_state += rules.get(current_state[idx:idx+5], '.')
    current_state = "...." + new_state + "...."  # Pad out non-plants on either end

# Count padding to get back to the original plant numbers
offset = int((len(current_state) - len(initial_state))/2)
answer = sum([idx-offset for idx, plant in enumerate(current_state) if plant=="#"])
print(f"Solution to part 1 is {answer}")

##############
# Solution 2 #
##############

# Find a pattern
old_answer = 0
current_state = "...." + initial_state + "...." # Pad out non-plants on either end
for step in range(1, 110):
    new_state = ""
    for idx in range(len(current_state)-4):  # Iterate as far as possible
        new_state += rules.get(current_state[idx:idx+5], '.')
    current_state = "...." + new_state + "...."  # Pad out non-plants on either end

    # Count padding to get back to the original plant numbers
    offset = int((len(current_state) - len(initial_state))/2)
    answer = sum([idx-offset for idx, plant in enumerate(current_state) if plant=="#"])
    
    # Compare to the previous step
    #print(step, answer, answer - old_answer)
    old_answer = answer

# On the 100 iterations it reaches a stable state, so no need to iterate 50 billion times:
num_steps = 50000000000
answer = 883 + num_steps * 51
print(f"Solution to part 2 is {answer}")
