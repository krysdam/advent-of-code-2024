from functools import lru_cache

TOWELS = []
DESIGNS = []

with open('input.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        if ',' in line:
            TOWELS = line.split(', ')
        else:
            DESIGNS.append(line)

@lru_cache(maxsize=None)
def how_many_ways(design):
    """How many ways can this design be made from the TOWELS?"""
    if design == '':
        return 1
    way_count = 0
    for towel in TOWELS:
        if design.startswith(towel):
            rest_of_design = design[len(towel):]
            way_count += how_many_ways(rest_of_design)
    return way_count

doable = 0
total_ways = 0
for design in DESIGNS:
    ways = how_many_ways(design)
    if ways > 0:
        doable += 1
        total_ways += ways

print(f'Part 1: {doable}')
print(f'Part 2: {total_ways}')