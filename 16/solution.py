from collections import defaultdict

grid = []
with open('input.txt', 'r') as f:
    for line in f:
        grid.append(list(line.strip()))

START = None
END = None
for r, row in enumerate(grid):
    for c, cell in enumerate(row):
        if cell == 'S':
            START = (r, c, 0, 1)
            grid[r][c] = '.'
        if cell == 'E':
            END = (r, c, 0, 0)
            grid[r][c] = '.'

def grid_index(grid, r, c):
    """Get the cell at this grid index. For out of bounds, return None."""
    if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
        return grid[r][c]
    return None

def grid_to_graph(grid):
    """Convert the grid to a graph representation."""
    turns = defaultdict(list)
    moves = defaultdict(list)
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell != '.':
                continue
            if (r, c) == END[:2]:
                continue
            # The four directions I can face from here
            face_north = (r, c, -1,  0)
            face_south = (r, c, +1,  0)
            face_east  = (r, c,  0, +1)
            face_west  = (r, c,  0, -1)
            # Turning options
            turns[face_north].extend([face_east, face_west])
            turns[face_south].extend([face_east, face_west])
            turns[face_east].extend([face_north, face_south])
            turns[face_west].extend([face_north, face_south])
            # Moving options
            for start in [face_north, face_south, face_east, face_west]:
                r, c, dr, dc = start
                landing = (r+dr, c+dc)
                # If we land at the end tile, don't include the direction
                if landing == END[:2]:
                    moves[start].append(END)
                # Otherwise, if we land on a '.' tile, include the direction
                elif grid_index(grid, r + dr, c + dc) == '.':
                    moves[start].append((r + dr, c + dc, dr, dc))
    return turns, moves

def dijkstra(turns, moves, start, end):
    """Run Dijkstra's algorithm to find the shortest path from start to every node."""
    dist = {start: 0}
    visited = set()
    queue = {start}
    while queue:
        current = min(queue, key=lambda x: dist[x])
        queue.remove(current)
        visited.add(current)
        for neighbor in turns[current]:
            if neighbor in visited:
                continue
            if dist.get(neighbor, float('inf')) > dist[current] + 1000:
                dist[neighbor] = dist[current] + 1000
                queue.add(neighbor)
        for neighbor in moves[current]:
            if neighbor in visited:
                continue
            if dist.get(neighbor, float('inf')) > dist[current] + 1:
                dist[neighbor] = dist[current] + 1
                queue.add(neighbor)
    return dist

def best_paths(turns, moves, start, end):
    """Find the best paths from start to end."""
    dist = dijkstra(turns, moves, start, end)
    paths = []
    def backtrack(path, current):
        if current == end:
            paths.append(path)
            return
        for neighbor in turns[current]:
            if dist.get(neighbor, float('inf')) == dist[current] + 1000:
                backtrack(path + [neighbor], neighbor)
        for neighbor in moves[current]:
            if dist.get(neighbor, float('inf')) == dist[current] + 1:
                backtrack(path + [neighbor], neighbor)
    backtrack([start], start)
    return paths

def good_seat_count(turns, moves, start, end):
    """Count the "good seats" (nodes on any best path)."""
    paths = best_paths(turns, moves, start, end)
    spots = set()
    for path in paths:
        for r, c, dr, dc in path:
            spots.add((r, c))
    return len(spots)


turns, moves = grid_to_graph(grid)
dist = dijkstra(turns, moves, START, END)[END]
print(f'Part 1: {dist}')
print(f'Part 2: {good_seat_count(turns, moves, START, END)}')