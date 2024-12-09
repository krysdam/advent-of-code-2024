# Read in the "dense format" disk map as given
with open('example.txt', 'r') as f:
    disk_map = f.read().strip()

# Decompress the map into its full form.
# The list represents the blocks of the disk in order, as in the problem.
# An int represents the file id contained there,
# and None represents empty space.
full_map = []
on_a_file = True
file_id = 0
for char in disk_map:
    length = int(char)
    if on_a_file:
        full_map.extend([file_id] * length)
        file_id += 1
    else:
        full_map.extend([None] * length)
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