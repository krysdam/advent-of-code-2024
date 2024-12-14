import re

WIDTH = 101
HEIGHT = 103

class Robot():
    def __init__(self, s):
        """Read the robot's parameters from a string like the input."""
        parts = re.match(r"p=(.+),(.+) v=(.+),(.+)", s).groups()
        parts = [int(x) for x in parts]
        self.x, self.y, self.vx, self.vy = parts

    def move(self):
        """Move the robot one step by its velocity."""
        self.x += self.vx
        self.y += self.vy
        self.x %= WIDTH
        self.y %= HEIGHT

    def quadrant(self):
        """Which quadrant is the robot in? If between, return None."""
        left  = self.x < WIDTH // 2
        right = self.x > WIDTH // 2
        up    = self.y < HEIGHT // 2
        down  = self.y > HEIGHT // 2
        if left and up:
            return 1
        if right and up:
            return 2
        if right and down:
            return 3
        if left and down:
            return 4
        return None
    
    def __repr__(self):
        return f"Robot({self.x}, {self.y}, {self.vx}, {self.vy})"
        
def safety_factor(robots):
    """The product of the robot-count in each quadrant."""
    quadrants = [0, 0, 0, 0]
    for robot in robots:
        q = robot.quadrant()
        if q is not None:
            quadrants[q-1] += 1
    product = 1
    for count in quadrants:
        product *= count
    return product

def robots_to_image(robots):
    """Convert the robots to a string image."""
    counts = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for robot in robots:
        counts[robot.y][robot.x] += 1
    image = ""
    for row in counts:
        for count in row:
            if count == 0:
                image += ".."
            else:
                image += f'{count:02}'
        image += "\n"
    return image


robots = []
# Read the full text of the input
with open('input.txt', 'r') as file:
    for line in file:
        line = line.strip()
        robots.append(Robot(line))

step_count = 0
while step_count < 100:
    for robot in robots:
        robot.move()
    step_count += 1
print(f'Part 1: {safety_factor(robots)}')


# Experimentally, the robots tend to cluster up every so often:
# They collect into a column at steps: 68, 169, 270... (increases by 101)
# They collect into a row at steps: 43, 146, 249... (increases by 103)
# We want the first step-number that fits both these patterns:
n = 0
while True:
    if (n - 68) % 101 == 0 and (n - 43) % 103 == 0:
        break
    n += 1
print(f'Part 2: {n}')

# Simulate that many steps and display the image
while step_count < n:
    for robot in robots:
        robot.move()
    step_count += 1
print(robots_to_image(robots))