from functools import lru_cache
import time

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

# Naive idea 3: It doesn't matter whether we do horizontal or vertical first,
#         (as long as the resulting sequence doesn't go off the edge).
#         There's no difference between (for example) >>^^^A and ^^^>>A,
#         because at the next level (assuming we start at A),
#         we either travel from A to > to ^ to A, or from A to ^ to > to A,
#         and by symmetry the path length is the same.
#         (And both orders clearly take 6 A presses).

# Correction for 3: It can matter.
#         It's true that the sequence is the same length (>^A vs ^>A),
#         and that the next level is the same length because
#         we either travel from A to > to ^ to A, or from A to ^ to > to A.
#         However, the next level after that can be different lengths.
#         Unfortunately this comment is too narrow to contain a proof of that.

# Repair for this problem: There is always some universally best order anyway.
#         For example, "if you're moving up and left, move left before up."
#         Or perhaps the opposite. I found out by trying all 4 factorial orders.
#         Turns out one good rule is: downs, then rights, then lefts, then ups.

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

@lru_cache(maxsize=None)
def key_to_key_sequence(key1, key2):
    """Return the "best" sequence that gets from key1 to key2.

    There are many possible paths, and possibly some are equally good,
    but this function produces one that is optimal.
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
    # This somehow guarantees the shortest sequence. See above.
    # In fact there are 6 orders like this (drlu, dlur, dlru, ludr, ldur, ldru).
    # I'm not exactly sure why this happens.
    # Seems like the requirements are: down before right, left before up,
    # and otherwise the order is irrelevant.
    # I'm sure it has something to do with the arrangement of the
    # directional pad, but I'm not sure exactly what.


def sequence(code):
    """Return the shortest sequence to produce the code."""
    current = 'A'
    path = ''
    for destination in code:
        path += key_to_key_sequence(current, destination) + 'A'
        current = destination
    return path


def sequence_with_intermediaries(code, intermediaries=0):
    """Return the shortest sequence to produce the code via intermediaries.
    
    Intermediaries in the problem are robots.
    Zero intermediaries means: return the code directly.
    One intermediary means: return the motions to type the code.
    Two intermediaries means: return the motions to type those motions.
    """
    result = code
    last_result = time.time()
    for r in range(intermediaries):
        result = sequence(result)
        delay = time.time() - last_result
        last_result = time.time()

        print(f'Level {r+1}: {len(result)} (took {delay:.2f}s)')
    return result


def complexity(code, intermediaries=0):
    """The complexity of the code (sequence length * numerical part)."""
    length = len(sequence_with_intermediaries(code, intermediaries))
    numeric_part = int(code[:-1])
    print(code, length, numeric_part)
    return length * numeric_part


codes = []
with open('input.txt', 'r') as f:
    for line in f:
        line = line.strip()
        codes.append(line)

# Note that the problem emphasizes the "two" robots,
# but there are definitelly *three* intermediaries.
# If I were entering the door code, that would be 0 intermediaries.
# The situation is that plus three robots in between.
# To put it another way, there are as many intermediaries
# as there are directional pads (each adds one layer of abstraction).
# So there are 3.
total = 0
for code in codes:
    total += complexity(code, intermediaries=3)
print(f'Part 1: {total}')
print('\n')

# In part 2, again the problem emphasizes there are "25" robots,
# but for the same reasons this is 26 intermediaries.
total = 0
for code in codes:
    total += complexity(code, intermediaries=26)
print(f'Part 2: {total}')
print('\n')