# Read in the "dense format" disk map as given
with open('input.txt', 'r') as f:
    line = f.read().strip()
    disk_map = [int(c) for c in line]

# Decompress the map into its full form.
# The list represents the blocks of the disk in order, as in the problem.
# An int represents the file id contained there,
# and None represents empty space.
full_map = []
on_a_file = True
file_id = 0
for num in disk_map:
    if on_a_file:
        full_map.extend([file_id] * num)
        file_id += 1
    else:
        full_map.extend([None] * num)
    on_a_file = not on_a_file


# Now, fold the later file blocks backward into the earlier spaces,
# as described in the problem.

# First split the disk into the part that will end up filled
# and the part that will end up empty.
disk_usage = sum(1 for block in full_map if block is not None)
disk_to_fill = full_map[:disk_usage]
disk_to_empty = full_map[disk_usage:]

# Now, fold the extra file blocks back
for i, block in enumerate(disk_to_fill):
    if block is None:
        to_move = disk_to_empty.pop()
        while to_move is None:
            to_move = disk_to_empty.pop()
        disk_to_fill[i] = to_move


# Find the checksum
checksum = sum(i * x for i, x in enumerate(disk_to_fill))
print(f'Part 1: {checksum}')



# Empty regions between files. Map from starting index to size.
gaps = {}

# Files. Map from file id to (start index, size).
files = []

index = 0
for i, item in enumerate(disk_map):
    if i%2 == 0:
        # File
        files.append((index, item))
    else:
        # Gap
        gaps[index] = item
    index += item


for f, file in reversed(list(enumerate(files))):
    start, size = file
    # Try each potential gap before where the file is now
    for gap_start in range(0, start):
        # Check if the gap is big enough
        gap_size = gaps.get(gap_start, 0)
        if gap_size >= size:
            # Move the file to this gap
            files[f] = (gap_start, size)
            del gaps[gap_start]
            gaps[gap_start + size] = gap_size - size
            break

checksum = 0
for f, file in enumerate(files):
    start, size = file
    for block in range(start, start + size):
        checksum += block * f

print(f'Part 2: {checksum}')


# Turn gaps into an array
# Might also turn gaps into some smart arrangement by size