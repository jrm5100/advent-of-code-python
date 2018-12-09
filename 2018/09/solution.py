#!/usr/bin/python3

from collections import deque

##############
# Load input #
##############

num_players = 412
last_marble_score = 71646

def play_game(num_players, last_marble_score):
    """Play the game with num_players up to the last marble score"""
    # Model board as a deque with the latest marble on the end
    board = deque([0])
    scores = [0 for _ in range(num_players)]
    current_player = 1
    # Run through all the steps
    for marble in range(1, last_marble_score+1):
        if marble % 23 == 0:
            scores[current_player] += marble
            board.rotate(7)
            scores[current_player] += board.pop()
            board.rotate(-1)
        else:
            board.rotate(-1)
            board.append(marble)
        # Go to the next player (or back around to the 1st)
        current_player += 1
        if current_player == num_players:
            current_player = 0
    
    return max(scores)

##############
# Solution 1 #
##############

    
answer = play_game(num_players, last_marble_score)
print(f"Solution to part 1 is {answer}")

##############
# Solution 2 #
##############

answer = play_game(num_players, last_marble_score*100)
print(f"Solution to part 2 is {answer}")
