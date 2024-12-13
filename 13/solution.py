import re

# Read the full text of the input
with open('input.txt', 'r') as file:
    text = file.read()

CLAW_MACHINE_REGEX = r"""
Button A: X\+(\d+), Y\+(\d+)
Button B: X\+(\d+), Y\+(\d+)
Prize: X=(\d+), Y=(\d+)
""".strip()

class ClawMachine:
    def __init__(self, regex_tuple):
        """Create a claw machine from a tuple of regex groups."""
        parts = [int(x) for x in regex_tuple]
        self.ax, self.ay = parts[:2]
        self.bx, self.by = parts[2:4]
        self.prize_x, self.prize_y = parts[4:]

    def extract_all_from_text(text):
        """Make a list of claw machines from a text describing them like the input."""
        # Regex for descriptions of claw machines

        machines = re.findall(CLAW_MACHINE_REGEX, text)
        return [ClawMachine(machine) for machine in machines]
    
    def is_solveable(self):
        """Is the machine solveable? If so, at what cost?"""
        # We want to solve the system of equations:
        # a*ax + b*bx = prize_x
        # a*ay + b*by = prize_y
        # In linear algebra terms:
        # [ax bx] [a]  ---  [prize_x]
        # [ay by] [b]  ---  [prize_y]
        # This is solveable with Cramer's rule.
        det = self.ax*self.by - self.ay*self.bx
        # If the determinant is zero, the system is not solveable by this method...
        # and that situation is intentionally excluded from the input cases.
        if det == 0:
            return None
        # Apply Cramer's rule
        det_a = self.prize_x*self.by - self.prize_y*self.bx
        det_b = self.ax*self.prize_y - self.ay*self.prize_x
        a = det_a / det
        b = det_b / det
        # Check that a and b are non-negative integers
        if a < 0 or b < 0 or a % 1 != 0 or b % 1 != 0:
            return None
        # Return the cost of the solution
        return round(a)*3 + round(b)
    
    def __str__(self):
        s = "ClawMachine("
        s += f"A=({self.ax}, {self.ay}), "
        s += f"B=({self.bx}, {self.by}), "
        s += f"Prize=({self.prize_x}, {self.prize_y})"
        s += ")"
        return s
    
    def __repr__(self):
        return str(self)
    

machines = ClawMachine.extract_all_from_text(text)
total = 0
for machine in machines:
    cost = machine.is_solveable()
    if cost is not None:
        total += cost

print(f'Part 1: {total}')


total2 = 0
for machine in machines:
    machine.prize_x += 10000000000000
    machine.prize_y += 10000000000000
    cost = machine.is_solveable()
    if cost is not None:
        total2 += cost

print(f'Part 2: {total2}')