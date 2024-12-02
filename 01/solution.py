# Read the left list and the right list.
left_list = []
right_list = []

with open("input.txt", "r") as f:
    for line in f:
        line = line.strip()
        halves = line.split()
        left_list.append(int(halves[0]))
        right_list.append(int(halves[1]))

# Sort them (smallest first, then next smallest...)
left_list = sorted(left_list)
right_list = sorted(right_list)

# Part 1: Find the total pairwise difference
total = 0
for left, right in zip(left_list, right_list):
    total += abs(left - right)

print(f"Part 1: {total}")


# Part 2: Find the "similarity score"
# Actually, the task is equivalent to summing the right list numbers
# that appear anywhere in the left list.

similarity = 0
for r in right_list:
    if r in left_list:
        similarity += r

print(f"Part 2: {similarity}")