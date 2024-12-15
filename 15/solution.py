import time

ROBOT= '@'
WALL = '#'
BOX = 'O'
BOX_LEFT = '['
BOX_RIGHT = ']'
SPACE = '.'


# Read the grid and commands as they are (list of strings and one long string)
grid = []
commands = ""
with open('input.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        if line[0] == WALL:
            grid.append(list(line))
        else:
            commands += line

def grid_index(grid, r, c):
    if 0 <= r < len(grid):
        if 0 <= c < len(grid[0]):
            return grid[r][c]
    return WALL

def print_grid(grid, sep=''):
    for row in grid:
        print(sep.join(row))
    print()

def find_robot(grid):
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == ROBOT:
                return (r, c)
    return None

def can_push(grid, r, c, dr, dc):
    """Check if the robot can push that location in that direction.
    
    Policy: if you push into someone,
    ask if they can_push, and also ask anyone connected to them.
    When you get pushed, don't ask anyone connected to you,
    because that would lead to infinite recursion.
    """
    # If we're being pushed into our own other half,
    # don't even check. The result will be the same as the other half.
    #print("can_push", r, c, grid_index(grid, r, c), dr, dc)
    here = grid_index(grid, r, c)
    if here == BOX_RIGHT and dc == -1:
        return True
    if here == BOX_LEFT and dc == +1:
        return True
    # Check what's ahead of us. Wall is no, space is yes.
    ahead = grid_index(grid, r + dr, c + dc)
    if ahead == WALL:
        return False
    if ahead == SPACE:
        return True
    # A box can be pushed if what's ahead can be pushed.
    if ahead == BOX:
        return can_push(grid, r + dr, c + dc,     dr, dc)
    if ahead == BOX_LEFT:
        # A box's left side (notify the right side too).
        return (can_push(grid, r + dr, c + dc,     dr, dc) and
                can_push(grid, r + dr, c + dc + 1, dr, dc))
    if ahead == BOX_RIGHT:
        # A box's right side (notify the left side too).
        return (can_push(grid, r + dr, c + dc,     dr, dc) and
                can_push(grid, r + dr, c + dc - 1, dr, dc))
    return False

def push(grid, r, c, dr, dc):
    """Push the box at r, c in the direction dr, dc, and all cascading effects.
    
    Assumes that this cell actually can be pushed (call can_push first).
    """
    #print("push", r, c, grid_index(grid, r, c), dr, dc)
    # Before moving, notify the things we're pushing into...
    # ...unless that thing is our own other half,
    # which would already have been notified to move by what pushed us.
    here = grid_index(grid, r, c)
    if not ((here == BOX_RIGHT and dc == -1) or
            (here == BOX_LEFT and  dc == +1)):
        ahead = grid_index(grid, r + dr, c + dc)
        # Inform whatever is ahead of us to be pushed as well
        if ahead == BOX:
            # A box is pushed
            push(grid, r + dr, c + dc, dr, dc)
        if ahead == BOX_LEFT:
            # A box's left is pushed, and we push its right side too
            push(grid, r + dr, c + dc + 1, dr, dc)
            push(grid, r + dr, c + dc,     dr, dc)
        if ahead == BOX_RIGHT:
            # A box's right is pushed, and we push its left side too
            push(grid, r + dr, c + dc - 1, dr, dc)
            push(grid, r + dr, c + dc,     dr, dc)
    # Finally we move ourselves into the new position
    grid[r + dr][c + dc] = grid[r][c]
    grid[r][c] = SPACE

def apply_commands(grid, commands):
    """Follow the given commands on the given grid. Return the grid."""
    robot_r, robot_c = find_robot(grid)
    for command in commands:
        dr, dc = 0, 0
        if command == '^':
            dr = -1
        elif command == 'v':
            dr = 1
        elif command == '<':
            dc = -1
        elif command == '>':
            dc = 1
        else:
            print(f"Invalid command: {command}")
            continue
        if can_push(grid, robot_r, robot_c, dr, dc):
            push(grid, robot_r, robot_c, dr, dc)
            robot_r += dr
            robot_c += dc
        #print_grid(grid)
        #time.sleep(0.1)
    return grid

def grid_gps_total(grid):
    """Total the "GPS" coordinates of the boxes."""
    total = 0
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == BOX or cell == BOX_LEFT:
                total += 100 * r + c
    return total

def double_grid(grid):
    """Reinterpret this grid as double-width, per Part 2."""
    new_grid = []
    for row in grid:
        new_row = []
        for cell in row:
            if cell == BOX:
                new_row.append(BOX_LEFT)
                new_row.append(BOX_RIGHT)
            elif cell == ROBOT:
                new_row.append(ROBOT)
                new_row.append(SPACE)
            else:
                new_row.append(cell)
                new_row.append(cell)
        new_grid.append(new_row)
    return new_grid


grid_part_1 = grid
grid_part_2 = double_grid(grid_part_1)

apply_commands(grid_part_1, commands)
print(f'Part 1: {grid_gps_total(grid_part_1)}')

apply_commands(grid_part_2, commands)
print(f'Part 2: {grid_gps_total(grid_part_2)}')