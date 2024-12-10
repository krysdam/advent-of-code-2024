# Read in the "dense format" disk map as given
with open('input.txt', 'r') as f:
    line = f.read().strip()
    dense_map = [int(c) for c in line]


def decompress(dense_map):
    """Convert dense disk format to list of block contents.

    An int represents the file id contained there,
    and None represents empty space.
    Sample input: "12345"
    Output: [0, None, None, 1, 1, 1, None, None, None, None, 2, 2, 2, 2, 2]
    """
    full_map = []
    on_a_file = True
    file_id = 0
    for num in dense_map:
        if on_a_file:
            full_map.extend([file_id] * num)
            file_id += 1
        else:
            full_map.extend([None] * num)
        on_a_file = not on_a_file
    return full_map

def defrag_by_block(block_map):
    """Defrag a disk map, "folding" the later files into early gaps, block by block.
    
    This is the defragging algorithm for part 1.
    """
    # First split the disk into the part that will end up filled
    # and the part that will end up empty.
    disk_usage = sum(1 for block in block_map if block is not None)
    disk_to_fill = block_map[:disk_usage]
    disk_to_empty = block_map[disk_usage:]

    # Now, fold the extra file blocks back
    for i, block in enumerate(disk_to_fill):
        if block is None:
            to_move = disk_to_empty.pop()
            while to_move is None:
                to_move = disk_to_empty.pop()
            disk_to_fill[i] = to_move

    # Return the filled first portion of the disk
    return disk_to_fill

def checksum(block_map):
    """Calculate the checksum of a disk map.
    
    The checksum is the sum of the block index times the block value.
    """
    return sum(i * block for i, block in enumerate(block_map))


# Part 1
block_map = decompress(dense_map)
block_map = defrag_by_block(block_map)
checksum = checksum(block_map)
print(f'Part 1: {checksum}')


def dense_map_to_files_and_gaps(dense_map):
    """Convert a dense map to a list of files and a dict of gaps.
    
    files is a list of (start index, size) tuples.
    gaps is a dict mapping start index to size.
    """
    gaps = {}
    files = []
    index = 0
    for i, item in enumerate(dense_map):
        if i % 2 == 0:
            # File
            files.append((index, item))
        else:
            # Gap
            gaps[index] = item
        index += item
    return files, gaps

def files_to_checksum(files):
    """Calculate the checksum of a list of files."""
    checksum = 0
    for f, (start, size) in enumerate(files):
        for block in range(start, start + size):
            checksum += block * f
    return checksum

def defrag_by_file(files, gaps):
    """Defrag a disk map, moving files into gaps, file by file.
    
    This is the defragging algorithm for part 2.
    """
    for f, (start, size) in reversed(list(enumerate(files))):
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
    return files, gaps

# Part 2
files, gaps = dense_map_to_files_and_gaps(dense_map)
files, gaps = defrag_by_file(files, gaps)

checksum = files_to_checksum(files)
print(f'Part 2: {checksum}')