import time

WALL = '#'
AIR = '.'

# Read the queue of falling blocks as tuples of (x, y) coordinates
falling_queue = []
with open('input.txt', 'r') as f:
    for line in f:
        x, y = map(int, line.split(','))
        falling_queue.append((x, y))


def print_grid(grid, path=None):
    """Print a grid visually, with optional path highlighted."""
    print('\n')
    for r in range(71):
        for c in range(71):
            if path and (r, c) in path:
                print('O', end=' ')
            else:
                print(grid[r][c], end=' ')
        print()

def grid_index(grid, r, c):
    """Fetch a grid index, returning None if out of bounds."""
    if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
        return grid[r][c]
    return None

def find_path(grid, start, end):
    """Find a path of AIR from start to end in the grid."""
    # Build predecessor dict until end is reached
    frontier = [start]
    predecessor = {start: None}
    cost_to = {start: 0}
    while frontier:
        current = frontier.pop(0)
        if current == end:
            break
        r, c = current
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if grid_index(grid, r+dr, c+dc) == AIR:
                next = (r+dr, c+dc)
                new_cost = cost_to[current] + 1
                if next not in cost_to or new_cost < cost_to[next]:
                    cost_to[next] = new_cost
                    frontier.append(next)
                    predecessor[next] = current
    # If end was never reached, return False
    if end not in predecessor:
        return False
    # Reconstruct path to end
    path_to_end = []
    current = end
    while current != start:
        path_to_end.append(current)
        current = predecessor[current]
    path_to_end.reverse()
    # Return the path
    return path_to_end

def grid_after_n_walls(falling_queue, n):
    """Return a grid with the first n falling blocks."""
    grid = [[AIR for x in range(71)] for y in range(71)]
    for (x, y) in falling_queue[:n]:
        grid[y][x] = WALL
    return grid

def path_after_n_walls(falling_queue, n):
    """Return the length of the path from (0, 0) to (70, 70) after n walls."""
    grid = grid_after_n_walls(falling_queue, n)
    path = find_path(grid, (0, 0), (70, 70))
    if path:
        return len(path)
    return -1

def path_exists(falling_queue, n):
    """Does a path exist from (0, 0) to (70, 70) after n walls?"""
    return path_after_n_walls(falling_queue, n) != -1

def binary_search(lo, hi, criteria):
    """Return the first n in [lo, hi) that satisfies criteria."""
    while lo < hi:
        mid = (lo + hi) // 2
        if criteria(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


# Part 1: Path length after 1024 walls have landed
print(f'Part 1: {path_after_n_walls(falling_queue, 1024)}')

# Part 2: First wall that prevents any path to the end
n = binary_search(0, len(falling_queue),
                  lambda n: not path_exists(falling_queue, n))
key_block = falling_queue[n-1]
print(f'Part 2: {key_block[0]},{key_block[1]}')