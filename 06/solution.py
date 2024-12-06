# Extract the grid as a list of strings
grid = []

with open('input.txt', 'r') as f:
    for line in f:
        grid.append(line.strip())

# Find the width, height, list of obstacle (x, y) coordinates,
# and position and direction of the guard.
# The origin is at the bottom left of the original file.
grid_width = len(grid[0])
grid_height = len(grid)

obstacles = {}
guard_pos = None
guard_dir = None

# For ease of indexing, flip the grid vertically
grid.reverse()

# Parse the grid
for y, row in enumerate(grid):
    for x, cell in enumerate(row):
        if cell == '#':
            obstacles[(x, y)] = True
        elif cell == '.':
            pass
        elif cell in ['^', 'v', '<', '>']:
            guard_pos = (x, y)
            guard_dir = {'^': (0, 1),
                         'v': (0, -1),
                         '<': (-1, 0),
                         '>': (1, 0)}[cell]
            
def guard_path(grid_width, grid_height, obstacles, guard_pos, guard_dir):
    """What tiles does the guard visit before leaving the grid, and is it a loop?
    
    Returns: (the set of visited tiles, boolean whether the guard is in a loop).
    """
    # Keep track of the cells visited by the guard
    visited = {guard_pos}

    # Also keep track of guard states. A guard state is (position, direction).
    # If the guard ever repeats a state, we know she's in a loop.
    visited_states = {(guard_pos, guard_dir)}

    def add_pos(pos1, pos2):
        return (pos1[0] + pos2[0], pos1[1] + pos2[1])

    def in_range(pos, width, height):
        return 0 <= pos[0] < width and 0 <= pos[1] < height

    # Propogate the guard until she leaves the grid
    while True:
        ahead = add_pos(guard_pos, guard_dir)
        # If you face an obstacle, turn right
        if ahead in obstacles:
            guard_dir = (guard_dir[1], -guard_dir[0])
        # If you're about to leave, the simulation is over
        elif not in_range(ahead, grid_width, grid_height):
            break
        # Otherwise, just step forward
        else:
            guard_pos = ahead
            visited.add(guard_pos)
            # If we've been here before, the guard is in a loop
            if (guard_pos, guard_dir) in visited_states:
                return visited, True
            visited_states.add((guard_pos, guard_dir))
    return visited, False

def count_looping_options(grid_width, grid_height, obstacles, guard_pos, guard_dir):
    """How many different added obstacles would put the guard in a loop?"""
    count = 0
    # Note we only have to count tiles the guard actually visited.
    visited, _ = guard_path(grid_width, grid_height, obstacles, guard_pos, guard_dir)
    for additional_obstacle in visited:
        # Presumably we can't put an obstacle where the guard starts
        if additional_obstacle == guard_pos:
            continue
        # Otherwise, add the obstacle and see if the guard loops
        hypothetical_obstacles = obstacles.copy()
        hypothetical_obstacles[additional_obstacle] = True
        _, looping = guard_path(grid_width, grid_height, hypothetical_obstacles, guard_pos, guard_dir)
        if looping:
            count += 1
    return count


# Print the number of visited cells
print(f"Part 1: {len(guard_path(grid_width, grid_height, obstacles, guard_pos, guard_dir)[0])}")
# Print the number of obstacles that would cause the guard to loop
print(f"Part 2: {count_looping_options(grid_width, grid_height, obstacles, guard_pos, guard_dir)}")