#!/usr/bin/python3

##############
# Load input #
##############

# Initialize data
board = "37"
elf1 = 0
elf2 = 1

##############
# Solution 1 #
##############

def next_10(board: str, elf1: int, elf2: int, prior_recipes: int) -> str:
    """Return the 10 scores appearing after the given number of scores"""
    while len(board) < prior_recipes + 10:
        # Move elves
        elf1 = (elf1 + int(board[elf1]) + 1) % len(board)
        elf2 = (elf2 + int(board[elf2]) + 1) % len(board)
        # Update scores
        board += str(int(board[elf1]) + int(board[elf2]))
    return board[-10:]

answer = next_10(board, elf1, elf2, 864801)
print(f"Solution to part 1 is {answer}")

##############
# Solution 2 #
##############

# I was initially stuck because I didn't consider that the sequence might be added with
# an extra digit after it, so the sequence might not appear at the very end of the board.
# This made me waste time trying to optimize things, thinking the answer was > 500 million

board = "37"
elf1 = 0
elf2 = 1

def number_to_left(board:str, elf1: int, elf2: int, sequence: str) -> int:
    """Return the number of scores appearing before the given sequence"""
    while sequence not in board[-len(sequence)-1:]:
        # Move elves
        elf1 = (elf1 + int(board[elf1]) + 1) % len(board)
        elf2 = (elf2 + int(board[elf2]) + 1) % len(board)
        # Update scores
        board += str(int(board[elf1]) + int(board[elf2]))
    return board.find(sequence)
    
answer = number_to_left(board, elf1, elf2, "864801")

print(f"Solution to part 2 is {answer}")
