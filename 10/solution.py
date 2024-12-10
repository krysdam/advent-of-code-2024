# Read in the grid as a list of lists of ints
grid = []
with open('input.txt', 'r') as f:
    for line in f:
        grid.append([int(char) for char in line.strip()])


def grid_index(grid, r, c):
    """Get the value at the given row and column in the grid."""
    if 0 <= r < len(grid):
        if 0 <= c < len(grid[r]):
            return grid[r][c]
    return None

def grid_to_graph(grid):
    """Convert a grid to a map of grid cells to connected cells.
    
    A cell is "connected" to another if they are directly adjacent
    and differ by +1 (the step must increase by 1).
    """
    graph = {}
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            graph[(r, c)] = []
            for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                neighbor = r + dr, c + dc
                if grid_index(grid, *neighbor) == cell + 1:
                    graph[(r, c)].append(neighbor)
    return graph

def trailhead_score(grid, graph, trailhead):
    """How many 9s are reachable from the given 0?"""
    # BFS from the trailhead outward
    visited = set()
    stack = [trailhead]
    while stack:
        current = stack.pop()
        visited.add(current)
        for neighbor in graph[current]:
            if neighbor not in visited:
                stack.append(neighbor)
    # Count 9s
    count = 0
    for r, c in visited:
        if grid_index(grid, r, c) == 9:
            count += 1
    return count

def total_score(grid):
    graph = grid_to_graph(grid)
    total = 0
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == 0:
                total += trailhead_score(grid, graph, (r, c))
    return total

def count_paths_to_nines(grid, graph, position):
    """How many paths from here lead to a 9?"""
    # Base case: 9s are terminal
    if grid_index(grid, *position) == 9:
        return 1
    # Count paths to 9s in neighbors
    count = 0
    for neighbor in graph[position]:
        count += count_paths_to_nines(grid, graph, neighbor)
    return count

def trailhead_rating(grid, graph, trailhead):
    """How many paths from the trailhead lead to a 9?"""
    return count_paths_to_nines(grid, graph, trailhead)

def total_rating(grid):
    graph = grid_to_graph(grid)
    total = 0
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == 0:
                total += trailhead_rating(grid, graph, (r, c))
    return total

print(f'Part 1: {total_score(grid)}')
print(f'Part 2: {total_rating(grid)}')