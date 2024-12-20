WALL = '#'
AIR = '.'


# Read the input grid from the file
grid = []
with open('input.txt', 'r') as f:
    for line in f:
        grid.append(list(line.strip()))

for r, row in enumerate(grid):
    for c, cell in enumerate(row):
        if cell == 'S':
            START = (r, c)
            grid[r][c] = AIR
        elif cell == 'E':
            END = (r, c)
            grid[r][c] = AIR


def grid_index(grid, r, c):
    """Return the value of the grid at (r, c), or None for out of bounds."""
    if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
        return grid[r][c]
    return None

def print_grid(grid, distances=None):
    """Print the grid, with distances if provided."""
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if distances and (r, c) in distances:
                print(distances[(r, c)] % 10, end='')
            else:
                print(cell, end='')
        print()

def distance_from_start(grid, start):
    """Return a dictionary of distances from the start point."""
    distances = {start: 0}
    queue = [start]
    while queue:
        r, c = queue.pop(0)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_r, new_c = r + dr, c + dc
            if grid_index(grid, new_r, new_c) == AIR and (new_r, new_c) not in distances:
                distances[(new_r, new_c)] = distances[(r, c)] + 1
                queue.append((new_r, new_c))
    return distances

def manhattan_distance(a, b):
    """Return the Manhattan distance between two points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def cheat_savings(grid, start, max_cheat_length = 2):
    """Return a list of the savings (in picoseconds) of each possible cheat."""
    distances = distance_from_start(grid, start)
    savings = []
    # For each possible point to start a cheat
    for r1, c1 in distances:
        # For each possible point to end this cheat
        for r2 in range(r1 - max_cheat_length, r1 + max_cheat_length + 1):
            for c2 in range(c1 - max_cheat_length, c1 + max_cheat_length + 1):
                # Make sure we're ending up on the track
                if grid_index(grid, r2, c2) != AIR:
                    continue
                # Make sure the cheat is not too long
                cheat_length = manhattan_distance((r1, c1), (r2, c2))
                if cheat_length > max_cheat_length:
                    continue
                # How much further ahead are we after the cheat?
                got_ahead_by = distances[(r2, c2)] - distances[(r1, c1)]
                # Discount the savings by the length of the cheat itself
                cheat_savings = got_ahead_by - cheat_length
                # If the cheat is worth something, add it to the list
                if cheat_savings > 0:
                    savings.append(cheat_savings)
    return savings

def count_cheats_over_100(grid, start, max_cheat_length = 2):
    """Return the number of cheats that save at least 100 picoseconds."""
    cheats = cheat_savings(grid, start, max_cheat_length)
    cheats_over_100 = [c for c in cheats if c >= 100]
    return len(cheats_over_100)


print(f'Part 1: {count_cheats_over_100(grid, START)}')
print(f'Part 2: {count_cheats_over_100(grid, START, max_cheat_length=20)}')