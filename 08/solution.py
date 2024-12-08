from collections import defaultdict

# Read in the grid as a list of strings
grid = []
with open('input.txt', 'r') as f:
    for line in f:
        grid.append(line.strip())

grid_width = len(grid[0])
grid_height = len(grid)

# Extract the antennas by frequency
# For each frequency (letter), a list of the coordinates of the antennas
# The origin is at the top left of the original grid
antennas = defaultdict(list)
for y, row in enumerate(grid):
    for x, cell in enumerate(row):
        if cell == '.':
            continue
        else:
            antennas[cell].append((x, y))

def in_grid(x, y, grid_width, grid_height):
    return 0 <= x < grid_width and 0 <= y < grid_height

def two_antinodes(ant1, ant2, grid_width, grid_height):
    """Return the coordinates of the (up to) two antinodes of the two antennas."""
    x1, y1 = ant1
    x2, y2 = ant2
    # The vector from ant1 to ant2
    dx = x2 - x1
    dy = y2 - y1
    # The extension from there beyond each antenna
    antinodes = [(x1 - dx, y1 - dy), (x2 + dx, y2 + dy)]
    # Filter out the antinodes that are outside the grid
    antinodes = [(x, y) for x, y in antinodes if in_grid(x, y, grid_width, grid_height)]
    return antinodes

def all_antinodes(ant1, ant2, grid_width, grid_height):
    """Return the coordinates of all antinodes of the two antennas."""
    antinodes = set()
    x1, y1 = ant1
    x2, y2 = ant2
    # The vector from ant1 to ant2
    dx = x2 - x1
    dy = y2 - y1
    # First, start at ant2 and continue "forwards"
    x, y = x2, y2
    while in_grid(x, y, grid_width, grid_height):
        antinodes.add((x, y))
        x += dx
        y += dy
    # Then, start at ant1 and continue "backwards"
    x, y = x1, y1
    while in_grid(x, y, grid_width, grid_height):
        antinodes.add((x, y))
        x -= dx
        y -= dy
    return antinodes

# Count up the unique antinodes of each type
total_simple_antinodes = set()
total_antinodes = set()
for frequency in antennas:
    for i, ant1 in enumerate(antennas[frequency]):
        for ant2 in antennas[frequency][i+1:]:
            simple_antinodes = two_antinodes(ant1, ant2, grid_width, grid_height)
            antinodes = all_antinodes(ant1, ant2, grid_width, grid_height)
            total_simple_antinodes.update(simple_antinodes)
            total_antinodes.update(antinodes)

print(f"Part 1: {len(total_simple_antinodes)}")
print(f"Part 2: {len(total_antinodes)}")