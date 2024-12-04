# Make a 2d array of the input
grid = []
with open('input.txt', 'r') as f:
    for line in f:
        grid.append(list(line.strip()))


def grid_get(g, r, c):
    """Return the char at row r, column c of grid g. Out of bounds is None."""
    if not (0 <= r < len(g)):
        return None
    if not (0 <= c < len(g[0])):
        return None
    return g[r][c]


def count_xmas(g):
    """Count instances of XMAS in g, as a wordsearch.
    
    Instances can be all eight directions: right, left, up, down,
    and all four diagonals.
    """
    count = 0
    # At every X...
    for r, row in enumerate(g):
        for c, cell in enumerate(row):
            if cell != 'X':
                continue
            # Check all eight directions
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    # Check if XMAS is in this direction
                    if (grid_get(g, r+dr, c+dc) == 'M' and
                        grid_get(g, r+2*dr, c+2*dc) == 'A' and
                        grid_get(g, r+3*dr, c+3*dc) == 'S'):
                        count += 1
    return count


def count_x_mas(g):
    """Count instances of MAS forming an X in g, as a wordsearch."""
    count = 0
    # At every A...
    for r, row in enumerate(g):
        for c, cell in enumerate(row):
            if cell != 'A':
                continue
            # Look one cell further along each diagonal.
            # The two opposite cells must be one M, one S.
            diag1 = {grid_get(g, r-1, c-1), grid_get(g, r+1, c+1)}
            diag2 = {grid_get(g, r-1, c+1), grid_get(g, r+1, c-1)}
            if diag1 == {'M', 'S'} and diag2 == {'M', 'S'}:
                count += 1
    return count



print(f"Part 1: {count_xmas(grid)}")
print(f"Part 2: {count_x_mas(grid)}")

