#!/usr/bin/python3

##############
# Load input #
##############

class Cart:
    # Dicts stored as class parameters to avoid a lot of if/else nesting
    cart_symbol_dict = {"^": "up", ">": "right", "v": "down", "<": "left"}
    reverse_symbol_dict = {v:k for k,v in cart_symbol_dict.items()}
    next_turn_dict = {'left': 'straight', 'straight': 'right', 'right': 'left'}
    curve_change_dir_dict = {
        "\\": {"up": "left", "right": "down", "down": "right", "left": "up"},
        "/": {"up": "right", "right": "up", "down": "left", "left": "down"}
    }
    perform_turn_dict = {
        'left': {'up': 'left', 'right': 'up', 'down': 'right', 'left': 'down'},
        'right': {'up': 'right', 'right': 'down', 'down': 'left', 'left': 'up'},
        'straight': {'up': 'up', 'right': 'right', 'down': 'down', 'left': 'left'},
    }
    
    def __init__(self, idx, x, y, symbol):
        self.idx = idx
        self.x = x
        self.y = y
        self.direction = self.cart_symbol_dict[symbol]
        self.crashed = False
        # Initialize intersection memory
        self.next_turn = 'left'

    def __repr__(self):
        symbol = self.reverse_symbol_dict[self.direction]
        return f"Cart(idx={self.idx}, x={self.x}, y={self.y}, {symbol})"

    def update_direction(self, track):
        track_state = track[self.y][self.x]
        if track_state in ("/", "\\"):
            # Turn due to the curve
            old = self.direction
            self.direction = self.curve_change_dir_dict[track_state][self.direction]
        elif track_state == "-":
            # Continue left or right
            assert self.direction in ("left", "right")
        elif track_state == "|":
            # Continue up or down
            assert self.direction in ("up", "down")
        elif track_state == "+":
            # Update direction based on the next turn and the current direction
            self.direction = self.perform_turn_dict[self.next_turn][self.direction]
            # Update the next turn
            self.next_turn = self.next_turn_dict[self.next_turn]
        else:
            # No other values possible
            raise ValueError(f"Track error: {track_state}")

    def tick(self, carts, track):
        # Move
        if self.direction == "up":
            self.y -= 1
        elif self.direction == "right":
            self.x += 1
        elif self.direction == "down":
            self.y += 1
        elif self.direction == "left":
            self.x -= 1

        # Update direction for the next tick
        self.update_direction(track)

        # Check for crashes
        other_live_carts_here = [
            c for c in carts
            if (c.x == self.x) & (c.y == self.y) & (c.idx != self.idx) & (not c.crashed)]
        if len(other_live_carts_here) > 0:
            self.crashed = True
            for c in other_live_carts_here:
                c.crashed = True

def load_data():
    track = []
    carts = []
    with open("input.txt", "r") as f:
        for y, line in enumerate(f):
            track_row = []
            for x, t in enumerate(line.replace("\n", "")):
                if t in "<>^v":
                    # Create cart
                    new_cart = Cart(len(carts), x, y, t)
                    carts.append(new_cart)
                    # Add track piece that is underneath
                    if new_cart.direction in ("up", "down"):
                        track_row.append("|")
                    elif new_cart.direction in ("left", "right"):
                        track_row.append("-")
                else:
                    # Add track piece
                    track_row.append(t)
            track.append(track_row)
    return track, carts

def print_track(track, carts):
    for y, row in enumerate(track):
        row_carts = {c.x:c for c in carts if c.y == y}
        row_symbols = ""
        for row_idx, t in enumerate(row):
            if row_idx in row_carts:
                row_symbols += Cart.reverse_symbol_dict[row_carts[row_idx].direction]
            else:
                row_symbols += t
        print(row_symbols)


##############
# Solution 1 #
##############

track, carts = load_data()

crash = False
while not crash:
    # Sort list of carts to process left to right and top to bottom
    carts = sorted(carts, key=lambda c: (c.x, c.y))
    # Update cart positions
    for c in carts:
        c.tick(carts, track)
        if c.crashed:
            # Break out after the first crash
            crash = True
            break
# Location of first crash
answer = f"{c.x},{c.y}"
print(f"Solution to part 1 is {answer}")

##############
# Solution 2 #
##############

track, carts = load_data()

while len(carts) > 1:
    # Sort list of carts to process left to right and top to bottom
    carts = sorted(carts, key=lambda c: (c.x, c.y))
    # Update cart positions
    for c in carts:
        if not c.crashed:
            # Skip updating a cart that crashed earlier in this round of ticks
            c.tick(carts, track)
    # keep only non-crashed carts
    carts = [c for c in carts if not c.crashed]

# Location of final cart
final_cart = carts[0]
answer = f"{final_cart.x},{final_cart.y}"
print(f"Solution to part 2 is {answer}")
