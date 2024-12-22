# Me <^v> Robot <^v> Robot <^v> Robot 0123456789 Door
#    level 3    level 2    level 1      level 0


# A level 0 code looks like 314A.
# A level 1 code looks like a loop of [ some ^<>v moves + A ].
# Every level past that has the same structure.

# Fact 1: The moves are some number of ^ or v, and some number of < or >.
#         The vertical movement is one of: ^^^, ^^, ^, nothing, v, vv, vvv.
#         The horizontal movement is one of: <<, <, nothing, >, >>.

# Fact 2: It's best to move all horizontal then all vertical, or vice versa,
#         and not any other order like ^>^^>.
#         The order doesn't change the length of the code,
#         but changing from (for example) ^ to > and back needlessly
#         will take extra moves on the next level.

# Fact 3: It doesn't matter whether we do horizontal or vertical first,
#         (as long as the resulting sequence doesn't go off the edge).
#         There's no difference between (for example) >>^^^A and ^^^>>A,
#         because at the next level (assuming we start at A),
#         we either travel from A to > to ^ to A, or from A to ^ to > to A,
#         and by symmetry the path length is the same.
#         (And both orders clearly take 6 A presses).

# Consequence of all this:
# For any starting key and destination key,
# there's only one path between them that is worth considering.
# For example from 1 to 9, we can define the path as ONLY >>^^,
# and ignore all other orders, and never recalculate it.

# 789
# 456
# 123
#  0A

NUMPAD = {
    '0': (3, 1),
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
    'gap': (3, 0),
}

#  ^A
# <v>

DIRPAD = {
    '^': (0, 1),
    '<': (1, 0),
    'v': (1, 1),
    '>': (1, 2),
    'A': (0, 2),
    'gap': (0, 0),
}

def key_to_key_path(key1, key2):
    """Return the "single worthwhile path" from key1 to key2.
    
    Other paths are possible, and maybe even equally good,
    but that doesn't matter (see above).
    """
    # Determine which keypad we're using: numpad or dirpad.
    if key1 == key2:
        return ''
    if key1 in NUMPAD and key2 in NUMPAD:
        pad = NUMPAD
    if key1 in DIRPAD and key2 in DIRPAD:
        pad = DIRPAD

    # How far right and down are we moving? (can be negative)
    y1, x1 = pad[key1]
    y2, x2 = pad[key2]
    rightward = (x2 - x1)
    downward  = (y2 - y1)

    # Make strings for each direction (note that at least two will be empty)
    right = '>' * max(0,  rightward)
    left  = '<' * max(0, -rightward)
    down  = 'v' * max(0,  downward)
    up    = '^' * max(0, -downward)

    # If moving horizontal first puts us on the gap, move vertical first.
    if (y1, x2) == pad['gap']:
        return (down + up)  +  (right + left)
    # If moving vertical first puts us on the gap, move horizontal first.
    if (y2, x1) == pad['gap']:
        return (right + left)  +  (down + up)
    
    # Otherwise use this magic order.
    return down + right + left + up
    #return down + right + left + up # THIS IS IT!!!!
    #return down + left + up + right # This one also works
    #return down + left + right + up # This also works
    #return left + up + down + right # This works
    #return left + down + up + right # This works
    #return left + down + right + up # This works

    

def path(code):
    current = 'A'
    path = ''
    for destination in code:
        path += key_to_key_path(current, destination) + 'A'
        current = destination
    return path


def complexity(code):
    length = len(path(path(path(code))))
    numeric_part = int(code[:-1])
    print(code, length, numeric_part)
    return length * numeric_part


codes = []
with open('input.txt', 'r') as f:
    for line in f:
        line = line.strip()
        codes.append(line)

total = 0

for code in codes:
    total += complexity(code)

print(f'Part 1: {total}')