import math
from functools import lru_cache

def num_length(n):
    """How many decimal digits does n have?"""
    if n == 0:
        return 1
    return int(math.log10(n)) + 1

def split_num(n):
    """Split a number into two halves by its digits."""
    halflen = num_length(n) // 2
    n_right = n % (10 ** halflen)
    n_left = n // (10 ** halflen)
    return n_left, n_right

@lru_cache(maxsize=None)
def count_stones(n, blinks):
    """A stone marked N will become how many stones after blink blinks?"""
    if blinks == 0:
        return 1
    # Rule 1: 0 becomes 1
    if n == 0:
        return count_stones(1, blinks - 1)
    # Rule 2: split even-digit numbers
    elif num_length(n) % 2 == 0:
        n1, n2 = split_num(n)
        return count_stones(n1, blinks - 1) + count_stones(n2, blinks - 1)
    # Rule 3: multiply other numbers by 2024
    else:
        return count_stones(n * 2024, blinks - 1)
    
def count_stone_line(stones, blinks):
    """These stones will become how many stones after blink blinks?"""
    return sum(count_stones(stone, blinks) for stone in stones)
    
with open('input.txt', 'r') as f:
    stones = [int(x) for x in f.read().split()]

print(f'Part 1: {count_stone_line(stones, 25)}')
print(f'Part 2: {count_stone_line(stones, 75)}')