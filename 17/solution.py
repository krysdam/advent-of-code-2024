class Computer():
    """A three-bit computer as described in the problem."""

    def __init__(self, a, b, c):
        # Initialize the registers
        self.a = a
        self.b = b
        self.c = c
        # Initialize the instruction pointer
        self.inst = 0
        # By default, don't print
        self.verbose = False

    def explain(self, msg, end='\n'):
        """Print a message, if verbose is True."""
        if self.verbose:
            print(msg, end=end)

    def combo(self, x):
        """The value of a "combo operand" as described in the problem."""
        return [0, 1, 2, 3, self.a, self.b, self.c, None][x]
    
    def adv(self, x):
        self.explain(f'A = A // 2**combo({x})')
        self.a = self.a // (2 ** self.combo(x))
        self.inst += 2

    def bxl(self, x):
        self.explain(f'B = B xor {x}')
        self.b = self.b ^ x
        self.inst += 2

    def bst(self, x):
        self.explain(f'B = combo({x}) % 8')
        self.b = self.combo(x) % 8
        self.inst += 2

    def jnz(self, x):
        self.explain(f'If a is not zero, jump to {x}\n\n\n')
        if self.a == 0:
            self.inst += 2
            return
        self.inst = x

    def bxc(self, x):
        self.explain(f'B = B xor C (ignore operand {x})')
        self.b = self.b ^ self.c
        self.inst += 2

    def out(self, x):
        self.explain(f'Output combo({x})')
        self.inst += 2
        return self.combo(x) % 8
    
    def bdv(self, x):
        self.explain(f'B = A // 2**combo({x})')
        self.b = self.a // (2 ** self.combo(x))
        self.inst += 2

    def cdv(self, x):
        self.explain(f'C = A // 2**combo({x})')
        self.c = self.a // (2 ** self.combo(x))
        self.inst += 2

    def run(self, program: list):
        """Run a program (list of ints) and return the output (list of ints)."""
        output = []
        commands = [self.adv, self.bxl, self.bst, self.jnz,
                    self.bxc, self.out, self.bdv, self.cdv]
        while self.inst < len(program):
            self.explain(f'[A={self.a:=10d}  B={self.b:10d}  C={self.c:10d}]', end='\t')
            cmd, operand = program[self.inst:self.inst+2]
            result = commands[cmd](operand)
            if result is not None:
                output.append(result)
        return output


# Read the initial register values and program
with open('input.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        name, thing = line.split(':')
        match name:
            case 'Register A':
                a = int(thing)
            case 'Register B':
                b = int(thing)
            case 'Register C':
                c = int(thing)
            case 'Program':
                program = [int(x) for x in thing.split(',')]
            case _:
                raise ValueError(f'Unknown line: {line}')
            
# Part 1
computer = Computer(a, b, c)
output = computer.run(program)
output = ','.join(map(str, output))
print(f'Part 1: {output}')


# Part 2
# Analysis of the program reveals:
# - It only loops once: from the end to the beginning, unless A = 0.
# - It only outputs once, from the value of B, at the end of each loop.
# - B and C are overwritten at the beginning of each loop.
# - A strictly decreases in every loop.
# So the program is a loop until A is 0, each time reducing A and outputting once.

def program_function(a, program):
    """A wrapper function for the given program."""
    computer = Computer(a, 0, 0)
    output = computer.run(program)
    return output

def produce_target_sequence(program, sequence):
    """Under certain assumptions, find an input A that produces the sequence.
    
    Assumption: the program is a loop until A is zero,
    each time reducing A by a factor of 8 and outputting once.
    """
    if sequence == []:
        return [0]
    to_produce_all_but_last = produce_target_sequence(program, sequence[1:])
    options = []
    for a in to_produce_all_but_last:
        for last_oct in range(8):
            test_a = a * 8 + last_oct
            output = program_function(test_a, program)
            if output == sequence:
                options.append(test_a)
    return options

# Part 2: Find the smallest A that makes program into a quine
print(f'Part 2: {min(produce_target_sequence(program, program))}')