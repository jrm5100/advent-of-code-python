#!/usr/bin/python3

from typing import List

##############
# Load input #
##############

class Elf:
    def __init__(self, idx, board):
        self.idx = idx
        self.board = board
        self.score = self.board[self.idx]
    
    def move(self):
        """Move the elf and return the next score"""
        self.idx += self.score + 1
        while self.idx >= len(board):
            self.idx -= len(board)
        self.score = self.board[self.idx]

# Initialize data
board = [3, 7]
elf1 = Elf(0, board)
elf2 = Elf(1, board)

##############
# Solution 1 #
##############

def next_10_simple(board: List[int], elf1: Elf, elf2: Elf, prior_recipes: int) -> str:
    """Return the 10 scores appearing after the given number of scores"""
    while len(board) < prior_recipes + 10:
        elf1.move()
        elf2.move()
        new_recipe = elf1.score + elf2.score
        for c in str(new_recipe):
            board.append(int(c))
    return "".join(str(n) for n in board[-10:])

answer = next_10_simple(board, elf1, elf2, 864801)
print(f"Solution to part 1 is {answer}")

##############
# Solution 2 #
##############

# Reset data to avoid checking the existing board, even though that would be more efficient
board = [3, 7]
elf1 = Elf(0, board)
elf2 = Elf(1, board)

def number_to_left(board: List[int], elf1: Elf, elf2: Elf, sequence: int) -> int:
    """Return the number of scores appearing before the given sequence"""
    sequence = [int(n) for n in str(sequence)]
    # TODO
    return len(board) - len(sequence)
    
answer = number_to_left(board, elf1, elf2, 864801)

print(f"Solution to part 2 is {answer}")
