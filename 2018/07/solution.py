#!/usr/bin/python3

##############
# Load input #
##############

def load_input():
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
    return requirements, incomplete_steps

##############
# Solution 1 #
##############

requirements, incomplete_steps = load_input()

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

# I should look into writing a solution using async/await.

# Reload data since the original data was altered
requirements, incomplete_steps = load_input()
completed_steps = ""
total_steps = len(incomplete_steps)

# Initialize worker tracking
seconds = 0
worker_tasks = [None, None, None, None, None]  # Which task is being done by each worker
worker_times = [0, 0, 0, 0, 0]  # Time remaining for current task for each worker

while len(completed_steps) < total_steps:
    # Pass the minimum time needed to free at least one worker
    nonzero_times = [n for n in worker_times if n != 0]  # Must ignore 0 as the minimum to avoid freezing time
    if len(nonzero_times) > 0:  # If all are zero the list will be empty and min() would return an error
        min_time_left = min(nonzero_times)
        seconds += min_time_left
        worker_times = [n-min_time_left if n > 0 else 0 for n in worker_times]

    # Process any completed jobs after this time has passed
    for idx in range(len(worker_tasks)):
        # Process available workers
        if worker_times[idx] == 0:
            if worker_tasks[idx] != None:
                # Mark the completed step (if there is one)
                completed_step = worker_tasks[idx]
                worker_tasks[idx] = None
                completed_steps += completed_step
                # Update requirements to remove the completed step
                requirements = {k:(v - set(completed_step)) for k,v in requirements.items()}

    # Get currently available tasks
    available_steps = set([step for step in incomplete_steps if len(requirements.get(step, set())) == 0])
            
    # Assign next alphabetical steps if possible
    for idx in range(len(worker_tasks)):
        if worker_tasks[idx] is None and len(available_steps) > 0:
            next_job = sorted(available_steps)[0]  # Get job
            worker_tasks[idx] = next_job  # Assign job
            incomplete_steps.remove(next_job)  # Remove job from incomplete steps
            available_steps.remove(next_job)  # Remove job from current list of available steps so subsequent workers don't use it this round
            next_job_time = ord(next_job) - 64 + 60  # ord("A") = 65 so next_job_time = 65 - 64 + 60 = 61
            worker_times[idx] = next_job_time  # Add time remaining for this new step

answer = seconds
print(f"Solution to part 2 is {answer}")
