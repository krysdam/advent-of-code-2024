# Read in the grid as a list of strings
with open('input.txt', 'r') as f:
    grid = f.read().splitlines()

def grid_index(grid, r, c):
    """Return the element at [r][c] or None for out of bounds."""
    if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
        return grid[r][c]
    return None

def get_region(grid, r, c):
    """The cells in the same region as this one.
    
    A region is a set of cells with the same letter,
    connected by orthogonal steps.
    """
    plant_type = grid_index(grid, r, c)
    region = set()
    # Depth-first search
    stack = [(r, c)]
    while stack:
        r, c = stack.pop()
        if grid_index(grid, r, c) == plant_type and (r, c) not in region:
            region.add((r, c))
            stack.extend([(r+1, c), (r-1, c), (r, c+1), (r, c-1)])
    return region

def get_regions(grid):
    """The regions of this garden.
    
    A region is a set of cells with the same letter,
    connected by orthogonal steps.
    """
    regions = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            for region in regions:
                if (r, c) in region:
                    break
            else:
                regions.append(get_region(grid, r, c))
    return regions

def region_area(region):
    """The number of cells in the region."""
    return len(region)

def region_perimeter(region):
    """The full perimeter of the region."""
    perimeter = 0
    for r, c in region:
        for neighbor in [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]:
            if neighbor not in region:
                perimeter += 1
    return perimeter

def region_corner_count(region):
    """The number of corners in the region."""
    # Draw a rectangle around the region.
    # Iterate over all the cells in that rectangle.
    # Count how many of those have a corner of the region
    # at their bottom right corner.
    corner_count = 0
    min_r = min(r for r, c in region)
    max_r = max(r for r, c in region)
    min_c = min(c for r, c in region)
    max_c = max(c for r, c in region)
    for r in range(min_r-1, max_r+1):
        for c in range(min_c-1, max_c+1):
            # Is there a corner at my bottom right?
            # This depends on which adjacent cells are in the region.
            # Specifically: (r, c), (r+1, c), (r, c+1), (r+1, c+1).
            top_left = (r, c) in region
            top_right = (r, c+1) in region
            bottom_left = (r+1, c) in region
            bottom_right = (r+1, c+1) in region
            # How many of these are in the region?
            in_count = top_left + top_right + bottom_left + bottom_right
            # If exactly one or three are in the region, there's a corner.
            if in_count in [1, 3]:
                corner_count += 1
            # If exactly four or none are in the region, there's no corner.
            elif in_count in [0, 4]:
                pass
            # If two diagonal cells are in the region, this is two corners.
            # (See the case about two interior regions making two corners).
            elif top_left and bottom_right or top_right and bottom_left:
                corner_count += 2
            # The other case is two adjacent, which is no corners.
    return corner_count

def region_score_by_perim(region):
    """The score of the region according to Part 1."""
    return region_area(region) * region_perimeter(region)

def region_score_by_sides(region):
    """The score of the region according to Part 2."""
    # A region's side count = its corner count.
    return region_area(region) * region_corner_count(region)

print(f'Part 1: {sum(region_score_by_perim(region) for region in get_regions(grid))}')
print(f'Part 2: {sum(region_score_by_sides(region) for region in get_regions(grid))}')