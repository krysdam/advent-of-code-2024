import itertools
from collections import defaultdict
import math
from functools import lru_cache

# Me <^v> Robot <^v> Robot <^v> Robot 0123456789 Door
#    step 3     step 2     step 1       step 0


# A step 0 code looks like 314A
# A step 1 code looks like a loop of [ (right/left) (up/down) move, then A ]
# A step 2 code is the same
# A step 3 code is the same

# How many directions for "19" are the shortest?
# I need to move right 2 and up 2, in any order: (4 2) = 6 ways
# Specifically these are A>>^^A, A>^>^A, A>^^>A, A^>>^A, A^>^>A, A^^>>A

# How many of these can possibly be shortest at the next level?
# The only possibly shortest ones are A>>^^A and A^^>>A = 2 ways
# Is it possible that these are tied?
# Yes, in fact they must be tied, because they are reverses of each other.

# In general:
# How many directions for "MN" are the shortest?

# Consider this:
# Manually make two lists
# What are the shortest free paths from M to N?     (as many as 9)
# What are the shortest "smooth" paths from M to N? (as many as 2)

# Part 1 = free(smooth(smooth(code)))

# 0    789
# 1    456
# 2    123
# 3     0A      ^ is on the same spot as 0
# 4    <v>

locations = {'0': (3, 1),
             '1': (2, 0),
             '2': (2, 1),
             '3': (2, 2),
             '4': (1, 0),
             '5': (1, 1),
             '6': (1, 2),
             '7': (0, 0),
             '8': (0, 1),
             '9': (0, 2),
             'A': (3, 2),
             '^': (3, 1),
             '<': (4, 0),
             'v': (4, 1),
             '>': (4, 2),
            }

NUMPAD = "0123456789A"
DIRPAD = "^<v>A"

STEPS = {'^': (-1, 0),
         '<': (0, -1),
         'v': (1, 0),
         '>': (0, 1),
        }


def manhattan_distance(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


@lru_cache(maxsize=None)
def a_to_b_free(start, end):
    if start == end:
        return {''}
    
    paths = []
    starty, startx = start
    distance = manhattan_distance(start, end)

    # Try all four directions
    for step in STEPS:
        dy, dx = STEPS[step]
        newy, newx = starty + dy, startx + dx
        # If we land on the gap at (3, 0), we can't go there
        if (newy, newx) == (3, 0):
            continue
        # Otherwise go anywhere that brings us closer to the end
        if manhattan_distance((newy, newx), end) < distance:
            paths += [step + path for path in a_to_b_free((newy, newx), end)]
    return set(paths)


def full_path_free(code):
    current = 'A'
    path = []
    for destination in code:
        path.append(a_to_b_free(locations[current], locations[destination]))
        path.append({'A'})
        current = destination
    return [''.join(x) for x in itertools.product(*path)]


def free(codes):
    result = []
    for code in codes:
        result += full_path_free(code)
    return result


@lru_cache(maxsize=None)
def a_to_b_smooth(start, end):
    if start == end:
        return {''}
    
    paths = []
    starty, startx = start
    endy, endx = end

    # Create the horizontal motion (like >> or <<<)
    # and vertical motion (like vv or ^^^)
    rightward = (endx - startx)
    downward = (endy - starty)
    horizontal = '>' * max(0, rightward) + '<' * max(0, -rightward)
    vertical =   'v' * max(0, downward)  + '^' * max(0, -downward)

    # If the horizontal move leaves us safe, we can do that first
    if (starty, endx) != (3, 0):
        paths.append(horizontal + vertical)
    # If the vertical move leaves us safe, we can do that first
    # (And possibly, we can do either)
    if (endy, startx) != (3, 0):
        paths.append(vertical + horizontal)

    return set(paths)


def full_path_smooth(code):
    current = 'A'
    path = []
    for destination in code:
        path.append(a_to_b_smooth(locations[current], locations[destination]))
        path.append({'A'})
        current = destination
    return [''.join(x) for x in itertools.product(*path)]


def smooth(codes):
    result = []
    for code in codes:
        result += full_path_smooth(code)
    return result


def complexity(code):
    options = list(free(smooth(smooth([code]))))
    shortest = min(options, key=len)
    length = len(shortest)

    numeric_part = int(code[:-1])

    return length * numeric_part


codes = []
with open('input.txt', 'r') as f:
    for line in f:
        line = line.strip()
        codes.append(line)

total = 0

for code in codes:
    print(code, complexity(code))
    total += complexity(code)

print(f'Part 1: {total}')