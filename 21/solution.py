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
#         Turns out one good rule is: any left, then vertical, then any right.
#         See this thread on the Reddit for a discussion of this fact:
#         reddit.com/r/adventofcode/comments/1hj7f89/
#         The gist appears to be that moving left before vertical
#         keeps all the left moves consecutive on later levels,
#         rather than moving all the way from A to < and back repeatedly.
#         The same reasoning applies to moving vertically before right.

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
    return left + up + down + right
    # This somehow guarantees the shortest sequence. See above.


def sequence(code):
    """Return the shortest sequence to produce the code."""
    current = 'A'
    path = ''
    for destination in code:
        path += key_to_key_sequence(current, destination) + 'A'
        current = destination
    return path


@lru_cache(maxsize=None)
def sequence_with_intermediaries(code, intermediaries=0):
    """Return the shortest seq length to produce the code via intermediaries.
    
    Intermediaries in the problem are robots.
    0 intermediaries means: return the code's length itself.
    1 intermediary means: return the number of motions to type the code.
    2 intermediaries means: return the number of motions to type those motions.
    """
    # With no intermediaries, the sequence length is the code's length.
    if intermediaries == 0:
        return len(code)
    # Split the code by A's, and find the sequence length to produce each one.
    length = 0
    segments = code.split('A')
    # If the code ends with A, splitting gives us a superfluous '' at the end.
    if segments[-1] == '':
        del segments[-1]
    # Add the A back into each segment.
    segments = [segment + 'A' for segment in segments]
    # Find each segment's length
    for segment in segments:
        length += sequence_with_intermediaries(sequence(segment),
                                               intermediaries-1)
    return length


def complexity(code, intermediaries=0):
    """The complexity of the code (sequence length * numerical part)."""
    length = sequence_with_intermediaries(code, intermediaries)
    numeric_part = int(code[:-1])
    #print(code, length, numeric_part)
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

# In part 2, again the problem emphasizes there are "25" robots,
# but for the same reasons this is 26 intermediaries.
total = 0
for code in codes:
    total += complexity(code, intermediaries=26)
print(f'Part 2: {total}')