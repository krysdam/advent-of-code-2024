class Equation():
    """An equation with the operators missing. Some answer equals some parts."""
    def __init__(self, string):
        answer, parts = string.split(': ')
        self.answer = int(answer)
        self.parts = [int(part) for part in parts.split(' ')]

def poperate(ls, op):
    """Combine the first two elements of a list using an operation."""
    return [op(ls[0], ls[1])] + ls[2:]

def solveable(answer, parts, operations):
    """Can we get the answer from the parts using the operations?"""
    # If there are somehow no parts, it's doomed
    if len(parts) == 0:
        return False
    # If we have one part, that's our result, and it should be the answer
    if len(parts) == 1:
        return parts[0] == answer
    # If we've already exceeded the answer, we can't get back down to it
    if parts[0] > answer:
        return False
    # Apply each operation to the first two parts and continue
    for op in operations:
        if solveable(answer, poperate(parts, op), operations):
            return True
    # If none of that worked, it's not possible
    return False

# The operations +, *, and ||
ADD = lambda x, y: x + y
MUL = lambda x, y: x * y
CON = lambda x, y: int(str(x) + str(y))

# Read the equations from the input file
equations = []
with open('input.txt', 'r') as f:
    for line in f:
        equations.append(Equation(line.strip()))

# Count the solveable equations
total_add_mul = 0
total_add_mul_con = 0
for e in equations:
    if solveable(e.answer, e.parts, [ADD, MUL]):
        total_add_mul += e.answer
    if solveable(e.answer, e.parts, [ADD, MUL, CON]):
        total_add_mul_con += e.answer

print(f'Part 1: {total_add_mul}')
print(f'Part 2: {total_add_mul_con}')