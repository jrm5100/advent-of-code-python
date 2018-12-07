#!/usr/bin/python3

##############
# Load input #
##############

incomplete_steps = set()  # incomplete steps, initalized to all steps
requirements = dict()  # map steps to the required steps that must be completed first
with open("input.txt", "r") as f:
    for line in f:
        step = line.split(' ')[7]
        prerequisite = line.split(' ')[1]

        # Make sure both are recorded, in case a step is only on one side of the rules
        incomplete_steps.add(step)
        incomplete_steps.add(prerequisite)

        if step not in requirements:
            requirements[step] = set(prerequisite)
        else:
            requirements[step].add(prerequisite)

##############
# Solution 1 #
##############

completed_steps = ""
while len(incomplete_steps) > 0:
    # Process any steps with no requirements
    for step in sorted(incomplete_steps):
        if len(requirements.get(step, set())) == 0:
            completed_steps += step
            incomplete_steps.remove(step)
            # Remove as prerequisite from others
            requirements = {k:(v - set(step)) for k,v in requirements.items()}
            break

answer = completed_steps
print(f"Solution to part 1 is {answer}")

##############
# Solution 2 #
##############

def tick(i, workers, remaining_steps):
    i += 1
    for idx in range(5):
        workers[idx] = (workers[idx][0], workers[idx][1] - 1)  # Current step, time left
        if workers[idx][1] <= 0:
            assigned_step = remaining_steps[0]
            remaining_steps = remaining_steps[1:]
            workers[idx] = (assigned_step, ord(assigned_step) - 64 + 60)  # ord(A) = 65
    return i, workers, remaining_steps

remaining_steps = answer  # From answer 1
i = 0
workers = [(None, 0), (None, 0), (None, 0), (None, 0), (None, 0)]  # Step, time remaining
while len(remaining_steps) > 0:
    i, workers, remaining_steps = tick(i, workers, remaining_steps)
    print(i, remaining_steps, workers)

# Add the longest remaining time
print(i)
i += max([w[1] for w in workers])

answer = i
print(f"Solution to part 2 is {answer}")
