from collections import defaultdict

FULL = (1<<24) - 1

def monkey_hash(n):
    """Return the result of the monkey's hash on the "secret" number n."""
    # Must be cropped after each operation
    # or else things from the left will move in and mess things up.
    n = (n ^ (n<<6)) & FULL
    n = (n ^ (n>>5)) & FULL
    n = (n ^ (n<<11)) & FULL
    n = n & FULL
    return n

def monkey_day(n):
    """Return the sequence of 2000 "secret" numbers starting with n."""
    sequence = [n]
    for _ in range(2000):
        n = monkey_hash(n)
        sequence.append(n)
    return sequence

def monkey_prices(n):
    """Return the sequence of 2000 monkey prices, starting from n."""
    return [num % 10 for num in monkey_day(n)]

def first_diffs(seq):
    """Return the first differences of the sequence."""
    return [seq[i+1] - seq[i] for i in range(len(seq)-1)]
    # Note for indexing:
    # Original sequence indexes:  0  1  2  3  4  5...
    # First differences are like:  01 12 23 34 45...
    # In other words, first_diffs[i] is the diff "to" seq[i],
    # not the diff "from" seq[i] to the next element.

def best_changes(ns):
    """Maximum number of bananas from monkeys with these secret numbers.
    
    See the problem statement for full explanation of that.
    """
    # For each sequence of four changes, the number of bananas achieved.
    changes_to_result = defaultdict(int)
    # For each monkey (their secret number n)
    for n in ns:
        # The sequences of changes that have already come up
        changes_seen = set()
        # The sequence of actual prices (digits) and first diffs
        prices = monkey_prices(n)
        diffs  = first_diffs(prices)
        for i in range(len(prices)-4):
            # The four previous changes, eg: (-1, -1, 0, +2)
            changes = tuple(diffs[i : i+4])
            price = prices[i+4]
            # If this is the first time we see that sequence of changes,
            # then using that sequence of changes will give us that price.
            # If we'd already seen it, we don't get more bananas.
            if changes not in changes_seen:
                changes_to_result[changes] += price
            changes_seen.add(changes)
    # The single best result achievable
    results = [changes_to_result[change] for change in changes_to_result]
    return max(results)


# Read initial secret numbers from the input
secrets = []
with open('input.txt', 'r') as f:
    for line in f:
        line = line.strip()
        price = int(line)
        secrets.append(price)

# Part 1: Sum of secret numbers after one day
after_one_day = sum(monkey_day(p)[-1] for p in secrets)
print(f'Part 1: {after_one_day}')

# Part 2: Most bananas possible for any sequence of changes
print(f'Part 2: {best_changes(secrets)}')