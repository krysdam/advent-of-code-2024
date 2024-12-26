# Collect all the keys and locks together,
# each as a list of strings.

keylocks = []
keylock = []

with open('input.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            keylocks.append(keylock)
            keylock = []
        else:
            keylock.append(line)
keylocks.append(keylock)

def compatible(kl1, kl2):
    """Are these two keys/locks compatible?
    
    Note that two keys can never be compatible,
    and two locks can never be compatible,
    even if we check them naively by just superimposing them,
    because all locks have the top row filled, and all keys, the bottom row.
    """
    for r in range(7):
        for c in range(5):
            if kl1[r][c] == '#' and kl2[r][c] == '#':
                return False
    return True

# Count the compatible pairs
pairs = 0
for i in range(len(keylocks)):
    kl1 = keylocks[i]
    for j in range(i):
        kl2 = keylocks[j]
        if compatible(kl1, kl2):
            pairs += 1
print(f'Part 1: {pairs}')