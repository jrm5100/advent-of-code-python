#!/usr/bin/python3

from queue import Queue

##############
# Load input #
##############

class Character:
    def __init__(self, x, y, kind, grid):
        self.x = x
        self.y = y
        self.kind = kind

        # Reference to the rest of the game
        self.grid = grid

        # Default starting values
        self.hitpoints = 200
        self.attack_power = 3

    def __repr__(self):
        return f"{self.kind} at {self.x},{self.y} with {self.hitpoints}hp"

    def __lt__(self, other):
        return self.y < other.y or (self.y == other.y and self.x < other.x)

    def iterate_grid(self):
        for row in self.grid:
            for t in row:
                yield t
    
    def iterate_characters(self):
        for row in self.grid:
            for tile in row:
                if tile[1] is not None:
                    yield tile[1]

    def get_surroundings(self):
        """Return surroundings in reading order (up, left, right, down)"""
        return [
            self.grid[self.y + 1][self.x],
            self.grid[self.y][self.x - 1],
            self.grid[self.y][self.x + 1],
            self.grid[self.y - 1][self.x]
            ]

    def find_targets(self):
        return [c for c in self.iterate_characters() if c.kind != self.kind]

    def find_target_range_tiles(self, targets):
        """Find open tiles surrounding targets"""
        tiles = set()
        for t in targets:
            # up
            (tile, char) = self.grid[t.y - 1][t.x]
            if (char is None and tile == ".") or char is self:
                tiles.add((t.x, t.y - 1))
            # left
            (tile, char) = self.grid[t.y][t.x - 1]
            if (char is None and tile == ".") or char is self:
                tiles.add((t.x - 1, t.y))
            # right
            (tile, char) = self.grid[t.y][t.x + 1]
            if (char is None and tile == ".") or char is self:
                tiles.add((t.x + 1, t.y))
            # down
            (tile, char) = self.grid[t.y + 1][t.x]
            if (char is None and tile == ".") or char is self:
                tiles.add((t.x, t.y + 1))

        return tiles

    def attack(self):
        """At least one target is in range"""
        surroundings = self.get_surroundings()
        surrounding_chars = [c for (t,c) in surroundings if c is not None]
        surrounding_chars = [c for c in surrounding_chars if c.kind != self.kind]

        # Return if no attack can be made
        if len(surrounding_chars) == 0:
            return
        # Attack the min-health character in reading order by selecting the first one with hitpoints == minimum
        target = [c for c in surrounding_chars if c.hitpoints == min([c.hitpoints for x in surrounding_chars])][0]
        self.grid[target.y][target.x][1].hitpoints -= self.attack_power
        if self.grid[target.y][target.x][1].hitpoints <= 0:
            self.grid[target.y][target.x][1] = None  

    def get_shortest_path(self, target_range_tiles):
        """Get the shortest path to a target"""
        # Use a queue of lists of coordinates
        q = Queue()
        q.put([(self.x, self.y)])
        visited = set((self.x, self.y))
        while not q.empty():
            current_path = q.get()
            (x, y) = current_path[-1]
            next_steps = [(x, y-1), (x-1, y), (x+1, y), (x, y+1)]
            for ns in next_steps:
                # Ensure next step is open and not already visited
                if self.grid[ns[1]][ns[0]] == [".", None] and ns not in visited:
                    updated_path = current_path + [ns]
                    if ns in target_range_tiles:
                        # Return if a target is found, since this will be the shortest so far
                        return updated_path
                    else:
                        # Otherwise add to the list of paths to extend
                        q.put(updated_path)
                        visited.add(ns)
        # Return None since the heap ran out without returning a path
        return None

    def move_to(self, x, y):
        """Process a move"""
        self.grid[y][x][1] = self
        self.grid[self.y][self.x][1] = None
        self.x = x
        self.y = y
    
    def move(self, target_range_tiles):
        """Move in the correct direction"""
        # Don't move if already in range
        if (self.x, self.y) in target_range_tiles:
            return
        shortest_path = self.get_shortest_path(target_range_tiles)
        if shortest_path is None:
            return
        first_step = shortest_path[1]  # 0 is the current position, 1 is the next one
        self.move_to(first_step[0], first_step[1])

    def take_turn(self):
        """Make the current character take it's turn"""
        targets = self.find_targets()
        target_range_tiles = self.find_target_range_tiles(targets)
        # Move if not in position to attack
        self.move(target_range_tiles)
        # Attack if in position to attack
        self.attack()


# Grid is a 2d array of lists, each with "#" or "." and None or a character
grid = []
with open("input.txt", "r") as f:
    for y, line in enumerate(f):
        row = []
        for x, c in enumerate(line.rstrip()):
            if c in "#.":
                # Add to the grid
                row.append([c, None])
            elif c in "GE":
                # Create a character
                character = Character(x, y, c, grid)
                row.append(['.', character])
        grid.append(row)       

def print_grid(grid, show_characters=False):
    # Create sorted copy of characters
    for row in grid:
        if show_characters:
            print("".join([t[0] if t[1] is None else t[1].kind for t in row]))
        else:
            print("".join([t[0] for t in row]))

print_grid(grid, True)


def process_battle(grid):
    completed_rounds = 0
    while True:
        # Get ordered list of characters at the start of the round
        characters = []
        for row in grid:
            for (_, character) in row:
                if character is not None:
                    characters.append(character)
        # Process characters
        for character in characters:
            # Check if targets are left, if not return the number of completed rounds
            targets_left = character.find_targets()
            if len(targets_left) == 0:
                return grid, completed_rounds
            character.take_turn()
        completed_rounds += 1
    return grid, completed_rounds

##############
# Solution 1 #
##############

grid, completed_rounds = process_battle(grid)

# TODO
remaining_hp = 0
for row in grid:
    for (tile, character) in row:
        if character is not None:
            remaining_hp += character.hitpoints

answer = completed_rounds * remaining_hp
print(f"Solution to part 1 is {answer}")

##############
# Solution 2 #
##############

answer = ""
print(f"Solution to part 2 is {answer}")
